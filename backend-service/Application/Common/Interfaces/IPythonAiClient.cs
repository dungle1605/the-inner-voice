using InnerVoice.Application.DTOs;

namespace InnerVoice.Application.Common.Interfaces;

public interface IPythonAiClient
{
    Task<string> GenerateChatResponseAsync(string message, List<ChatMessageDto> history, CancellationToken cancellationToken = default);
}
