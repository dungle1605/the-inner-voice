using InnerVoice.Application.DTOs;
using InnerVoice.Application.Services;
using InnerVoice.Domain.Entities;
using Microsoft.AspNetCore.Mvc;

namespace InnerVoice.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IChatService _chatService;

    public ChatController(IChatService chatService)
    {
        _chatService = chatService;
    }

    [HttpPost]
    public async Task<ActionResult<ChatResponseDto>> SendMessage([FromBody] ChatRequestDto request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Message))
        {
            return BadRequest(new { message = "Nội dung tin nhắn không được để trống." });
        }

        var result = await _chatService.HandleMessageAsync(request, cancellationToken);
        return Ok(result);
    }

    [HttpGet("history/{sessionId}")]
    public async Task<ActionResult<IEnumerable<ConversationLog>>> GetHistory(string sessionId, CancellationToken cancellationToken)
    {
        var logs = await _chatService.GetHistoryAsync(sessionId, cancellationToken);
        return Ok(logs);
    }

    [HttpGet("emergency-resources")]
    public ActionResult<IEnumerable<EmergencyResourceDto>> GetEmergencyResources()
    {
        var resources = _chatService.GetEmergencyResources();
        return Ok(resources);
    }
}
