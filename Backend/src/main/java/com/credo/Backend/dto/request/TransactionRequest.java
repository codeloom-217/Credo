
package com.credo.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Pattern;

public record TransactionRequest(

        @NotBlank
        String customer_id,

        @NotBlank
        @Pattern(
                regexp = "^\\d{4}-\\d{2}-\\d{2}$",
                message = "Transaction date must be in YYYY-MM-DD format"
        )
        String transaction_date,

        @NotBlank
@Pattern(
    regexp = "^(CREDIT|DEBIT)$",
    flags = Pattern.Flag.CASE_INSENSITIVE,
    message = "Transaction type must be CREDIT or DEBIT"
)
String transaction_type,

        @NotNull
        @PositiveOrZero
        Double amount,

        @NotNull
        @PositiveOrZero
        Double balance,

        @NotBlank
        String transaction_mode,

        @NotBlank
        String narration

) {}
