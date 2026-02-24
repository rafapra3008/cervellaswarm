/**
 * Billing Types for CervellaSwarm
 *
 * Type definitions for usage tracking and tier management.
 * Schema designed for local JSON storage with future-proofing.
 *
 * Copyright 2026 CervellaSwarm Contributors
 * Licensed under the Apache License, Version 2.0
 */
/**
 * Quota check status levels
 */
export var QuotaStatus;
(function (QuotaStatus) {
    QuotaStatus["OK"] = "ok";
    QuotaStatus["WARNING"] = "warning";
    QuotaStatus["EXCEEDED"] = "exceeded";
})(QuotaStatus || (QuotaStatus = {}));
//# sourceMappingURL=types.js.map