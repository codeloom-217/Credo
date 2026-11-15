
package com.credo.backend.client;

import com.credo.backend.config.MlServiceConfig;
import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.response.MlServiceResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MlServiceClient {

    private final RestClient restClient;

    public MlServiceClient(MlServiceConfig config) {
        this.restClient = RestClient.builder()
                .baseUrl(config.baseUrl())
                .build();
    }

    public MlServiceResponse score(ScoreRequest request) {

        RestClient.RequestBodySpec scoreRequest = restClient.post()
                .uri("/score");

        String correlationId = MDC.get("correlationId");

        if (correlationId != null && !correlationId.isBlank()) {
            scoreRequest.header("X-Correlation-ID", correlationId);
        }

        return scoreRequest
                .body(request)
                .retrieve()
                .body(MlServiceResponse.class);
    }

    public boolean isHealthy() {
        try {
            restClient.get()
                    .uri("/health")
                    .retrieve()
                    .toBodilessEntity();

            return true;
        } catch (Exception ex) {
            return false;
        }
    }
}
