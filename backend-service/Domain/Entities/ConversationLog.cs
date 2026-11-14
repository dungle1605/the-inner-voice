using InnerVoice.Domain.Enums;

namespace InnerVoice.Domain.Entities;

public class ConversationLog
{
    public int Id { get; set; }
    public string SessionId { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public string AnonymizedContent { get; set; } = string.Empty;
    public RiskLevel RiskLevel { get; set; } = RiskLevel.Low;
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}
