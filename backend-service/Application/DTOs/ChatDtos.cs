namespace InnerVoice.Application.DTOs;

public class ChatMessageDto
{
    public string Role { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

public class ChatRequestDto
{
    public string SessionId { get; set; } = Guid.NewGuid().ToString();
    public string Message { get; set; } = string.Empty;
    public List<ChatMessageDto> History { get; set; } = [];
}

public class ChatResponseDto
{
    public string Response { get; set; } = string.Empty;
    public string RiskLevel { get; set; } = "Low";
    public bool IsEmergency { get; set; } = false;
    public string? EmergencyHotline { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

public class EmergencyResourceDto
{
    public string Country { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Phone { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}
