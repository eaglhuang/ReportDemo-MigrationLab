namespace ReportDemo.Documents;

public enum ConversionDisposition
{
    Reused,
    Wrapped,
    Ported,
    Rewritten,
    DocumentedException
}

public sealed record ConversionMapEntry(
    string QutoraComponent,
    string SourcePath,
    string Behavior,
    ConversionDisposition Disposition,
    string Reason,
    string TargetTaskId);

public sealed class ConversionMapValidator
{
    public bool IsComplete(ConversionMapEntry entry)
    {
        ArgumentNullException.ThrowIfNull(entry);

        return !string.IsNullOrWhiteSpace(entry.QutoraComponent)
            && !string.IsNullOrWhiteSpace(entry.SourcePath)
            && !string.IsNullOrWhiteSpace(entry.Behavior)
            && !string.IsNullOrWhiteSpace(entry.Reason)
            && !string.IsNullOrWhiteSpace(entry.TargetTaskId);
    }
}

