namespace InnerVoice.Api.Data;

public class ConversationLog
{
    public int Id { get; set; }
    public string SessionId { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public string AnonymizedContent { get; set; } = string.Empty;
    public string RiskLevel { get; set; } = "Low";
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

