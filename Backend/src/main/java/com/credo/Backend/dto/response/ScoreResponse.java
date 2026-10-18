package com.credo.backend.dto.response;

public record ScoreResponse(
        String customerId,
        Integer credoScore,
        String riskBand,
        Integer predictedOutcome,
        Double predictedProbability
) {}