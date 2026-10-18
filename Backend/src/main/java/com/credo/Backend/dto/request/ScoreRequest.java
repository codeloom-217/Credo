package com.credo.backend.dto.request;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.util.List;

public record ScoreRequest(

        @NotEmpty
        @Size(max = 1000)
        List<@NotNull @Valid TransactionRequest> transactions

) {}