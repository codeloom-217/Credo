package com.credo.backend.client;

import com.credo.backend.config.MlServiceConfig;
import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.response.MlServiceResponse;
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
        return restClient.post()
                .uri("/score")
                .body(request)
                .retrieve()
                .body(MlServiceResponse.class);
    }
}
