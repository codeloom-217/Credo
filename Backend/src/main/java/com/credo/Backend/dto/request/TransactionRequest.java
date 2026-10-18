package com.credo.backend.dto.request;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;

public record TransactionRequest(

        @NotBlank
        String customer_id,

        @NotBlank
        String transaction_date,

        @NotBlank
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