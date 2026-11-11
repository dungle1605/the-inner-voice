namespace InnerVoice.Api.Models;

public class ChatRequest
{
    public string SessionId { get; set; } = Guid.NewGuid().ToString();
    public string Message { get; set; } = string.Empty;
    public List<ChatMessage> History { get; set; } = [];
}

