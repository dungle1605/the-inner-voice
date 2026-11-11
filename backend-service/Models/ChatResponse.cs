namespace InnerVoice.Api.Models;

public class ChatResponse
{
    public string Response { get; set; } = string.Empty;
    public string RiskLevel { get; set; } = "Low"; // Low, Moderate, High, Critical
    public bool IsEmergency { get; set; } = false;
    public string? EmergencyHotline { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

