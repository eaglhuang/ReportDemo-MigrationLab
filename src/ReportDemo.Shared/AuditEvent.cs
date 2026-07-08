namespace ReportDemo.Shared;

public sealed record AuditEvent(
    string EventType,
    string ActorId,
    string CorrelationId,
    string PayloadHash,
    DateTimeOffset CreatedAt);

