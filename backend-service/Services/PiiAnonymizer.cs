using System.Text.RegularExpressions;

namespace InnerVoice.Api.Services;

public interface IPiiAnonymizer
{
    string Anonymize(string text);
}

public class PiiAnonymizer : IPiiAnonymizer
{
    private static readonly Regex EmailRegex = new(@"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", RegexOptions.Compiled);
    private static readonly Regex PhoneRegex = new(@"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b", RegexOptions.Compiled);

    public string Anonymize(string text)
    {
        if (string.IsNullOrWhiteSpace(text)) return string.Empty;

        var sanitized = EmailRegex.Replace(text, "[EMAIL_REDACTED]");
        sanitized = PhoneRegex.Replace(sanitized, "[PHONE_REDACTED]");
        return sanitized;
    }
}

