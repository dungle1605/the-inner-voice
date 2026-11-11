using InnerVoice.Api.Data;
using InnerVoice.Api.Models;
using InnerVoice.Api.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace InnerVoice.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IPythonAiClient _aiClient;
    private readonly IPiiAnonymizer _anonymizer;
    private readonly AppDbContext _dbContext;
    private readonly ILogger<ChatController> _logger;

    // Các từ khóa rủi ro khẩn cấp (Crisis keywords) theo tiêu chuẩn bảo vệ an toàn vị thành niên
    private static readonly string[] CrisisKeywords =
    [
        "tự tử", "muốn chết", "tự sát", "cắt tay", "kết liễu",
        "suicide", "me tuer", "en finir", "mourir", "self-harm"
    ];

    public ChatController(
        IPythonAiClient aiClient,
        IPiiAnonymizer anonymizer,
        AppDbContext dbContext,
        ILogger<ChatController> logger)
    {
        _aiClient = aiClient;
        _anonymizer = anonymizer;
        _dbContext = dbContext;
        _logger = logger;
    }

    [HttpPost]
    public async Task<ActionResult<ChatResponse>> SendMessage([FromBody] ChatRequest request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Message))
        {
            return BadRequest(new { message = "Nội dung tin nhắn không được để trống." });
        }

        var lowerMessage = request.Message.ToLowerInvariant();
        var isCrisis = CrisisKeywords.Any(k => lowerMessage.Contains(k));
        var riskLevel = isCrisis ? "Critical" : "Low";

        string botReply;
        if (isCrisis)
        {
            botReply = "Mình rất lo lắng cho bạn và muốn bạn được an toàn. Cảm xúc bạn đang trải qua là có thật, nhưng bạn không phải đối mặt với nó một mình. Hãy kết nối ngay với người lớn bạn tin tưởng hoặc liên hệ đường dây hỗ trợ khẩn cấp miễn phí: Tổng đài Quốc gia Bảo vệ Trẻ em 111 (Việt Nam) hoặc 3114 (Numéro national de prévention du suicide - Pháp). Chúng mình luôn ở đây vì bạn.";
        }
        else
        {
            botReply = await _aiClient.GenerateChatResponseAsync(request.Message, request.History, cancellationToken);
        }

        // Lưu log ẩn danh hóa theo chuẩn GDPR phục vụ pipeline Data Fabric / Databricks
        var anonymizedUserMessage = _anonymizer.Anonymize(request.Message);
        
        _dbContext.ConversationLogs.AddRange(
            new ConversationLog
            {
                SessionId = request.SessionId,
                Role = "user",
                AnonymizedContent = anonymizedUserMessage,
                RiskLevel = riskLevel,
                Timestamp = DateTime.UtcNow
            },
            new ConversationLog
            {
                SessionId = request.SessionId,
                Role = "assistant",
                AnonymizedContent = botReply,
                RiskLevel = riskLevel,
                Timestamp = DateTime.UtcNow
            }
        );

        await _dbContext.SaveChangesAsync(cancellationToken);

        return Ok(new ChatResponse
        {
            Response = botReply,
            RiskLevel = riskLevel,
            IsEmergency = isCrisis,
            EmergencyHotline = isCrisis ? "VN: 111 / 1800 1567 | France: 3114 | Fil Santé Jeunes: 0 800 235 236" : null,
            Timestamp = DateTime.UtcNow
        });
    }

    [HttpGet("history/{sessionId}")]
    public async Task<ActionResult<IEnumerable<ConversationLog>>> GetHistory(string sessionId, CancellationToken cancellationToken)
    {
        var logs = await _dbContext.ConversationLogs
            .Where(c => c.SessionId == sessionId)
            .OrderBy(c => c.Timestamp)
            .ToListAsync(cancellationToken);

        return Ok(logs);
    }

    [HttpGet("emergency-resources")]
    public IActionResult GetEmergencyResources()
    {
        return Ok(new
        {
            vietnam = new[]
            {
                new { name = "Tổng đài Quốc gia Bảo vệ Trẻ em", phone = "111", description = "Tư vấn tâm lý, bảo vệ trẻ em và thanh thiếu niên 24/7 (Miễn phí)" },
                new { name = "Tổng đài Ngày Mai", phone = "096 306 1414", description = "Hỗ trợ người trầm cảm và khủng hoảng tâm lý" }
            },
            france = new[]
            {
                new { name = "Numéro National Prévention Suicide", phone = "3114", description = "Ligne d'écoute et d'intervention de crise 24h/24, 7j/7 (Gratuit)" },
                new { name = "Fil Santé Jeunes", phone = "0 800 235 236", description = "Écoute et soutien pour les jeunes de 12 à 25 ans" },
                new { name = "SOS Amitié", phone = "09 72 39 40 50", description = "Écoute bienveillante et anonyme" }
            }
        });
    }
}

