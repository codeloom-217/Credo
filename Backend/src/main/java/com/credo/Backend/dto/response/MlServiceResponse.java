
package com.credo.backend.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record MlServiceResponse(
        String status,
        List<Result> results
) {

    public record Result(
            @JsonProperty("customer_id")
            String customerId,

            @JsonProperty("credo_score")
            Integer credoScore,

            @JsonProperty("risk_band")
            String riskBand,

            @JsonProperty("predicted_outcome")
            Integer predictedOutcome,

            @JsonProperty("predicted_probability")
            Double predictedProbability
    ) {}
}
