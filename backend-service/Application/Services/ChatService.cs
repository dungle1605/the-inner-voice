using InnerVoice.Application.Common.Interfaces;
using InnerVoice.Application.DTOs;
using InnerVoice.Domain.Entities;
using InnerVoice.Domain.Enums;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace InnerVoice.Application.Services;

public interface IChatService
{
    Task<ChatResponseDto> HandleMessageAsync(ChatRequestDto request, CancellationToken cancellationToken = default);
    Task<List<ConversationLog>> GetHistoryAsync(string sessionId, CancellationToken cancellationToken = default);
    List<EmergencyResourceDto> GetEmergencyResources();
}

public class ChatService : IChatService
{
    private readonly IPythonAiClient _aiClient;
    private readonly IPiiAnonymizer _anonymizer;
    private readonly IAppDbContext _dbContext;
    private readonly ILogger<ChatService> _logger;

    private static readonly string[] CrisisKeywords =
    [
        "tự tử", "muốn chết", "tự sát", "cắt tay", "kết liễu", "không muốn sống",
        "suicide", "me tuer", "en finir", "mourir", "automutilation", "self-harm"
    ];

    public ChatService(
        IPythonAiClient aiClient,
        IPiiAnonymizer anonymizer,
        IAppDbContext dbContext,
        ILogger<ChatService> logger)
    {
        _aiClient = aiClient;
        _anonymizer = anonymizer;
        _dbContext = dbContext;
        _logger = logger;
    }

    public async Task<ChatResponseDto> HandleMessageAsync(ChatRequestDto request, CancellationToken cancellationToken = default)
    {
        var lowerMessage = request.Message.ToLowerInvariant();
        var isCrisis = CrisisKeywords.Any(k => lowerMessage.Contains(k));
        var riskLevel = isCrisis ? RiskLevel.Critical : RiskLevel.Low;

        string botReply;
        if (isCrisis)
        {
            _logger.LogWarning("Crisis keywords detected in user session: {SessionId}", request.SessionId);
            botReply = "Mình rất lo lắng cho bạn và muốn bạn được an toàn. Cảm xúc bạn đang trải qua là có thật, nhưng bạn không phải đối mặt với nó một mình. Hãy kết nối ngay với người lớn bạn tin tưởng hoặc liên hệ đường dây hỗ trợ khẩn cấp miễn phí: Tổng đài Quốc gia Bảo vệ Trẻ em 111 (Việt Nam) hoặc 3114 (Numéro national de prévention du suicide - Pháp). Chúng mình luôn ở đây vì bạn.";
        }
        else
        {
            botReply = await _aiClient.GenerateChatResponseAsync(request.Message, request.History, cancellationToken);
        }

        // GDPR PII Redaction
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

        return new ChatResponseDto
        {
            Response = botReply,
            RiskLevel = riskLevel.ToString(),
            IsEmergency = isCrisis,
            EmergencyHotline = isCrisis ? "VN: 111 / 1800 1567 | France: 3114 | Fil Santé Jeunes: 0 800 235 236" : null,
            Timestamp = DateTime.UtcNow
        };
    }

    public async Task<List<ConversationLog>> GetHistoryAsync(string sessionId, CancellationToken cancellationToken = default)
    {
        return await _dbContext.ConversationLogs
            .Where(c => c.SessionId == sessionId)
            .OrderBy(c => c.Timestamp)
            .ToListAsync(cancellationToken);
    }

    public List<EmergencyResourceDto> GetEmergencyResources()
    {
        return
        [
            new() { Country = "Việt Nam", Name = "Tổng đài Quốc gia Bảo vệ Trẻ em", Phone = "111", Description = "Tư vấn tâm lý, bảo vệ trẻ em và thanh thiếu niên 24/7 (Miễn phí)" },
            new() { Country = "Việt Nam", Name = "Đường dây nóng Ngày Mai", Phone = "096 306 1414", Description = "Hỗ trợ người trầm cảm và khủng hoảng tâm lý" },
            new() { Country = "France", Name = "Numéro National Prévention Suicide", Phone = "3114", Description = "Ligne d'écoute et d'intervention de crise 24h/24, 7j/7 (Gratuit)" },
            new() { Country = "France", Name = "Fil Santé Jeunes", Phone = "0 800 235 236", Description = "Écoute et soutien pour les jeunes de 12 à 25 ans" }
        ];
    }
}
