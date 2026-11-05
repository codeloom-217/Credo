
package com.credo.backend.service;

import com.credo.backend.client.MlServiceClient;
import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.response.MlServiceResponse;
import com.credo.backend.dto.response.ScoreResponse;
import com.credo.backend.entity.ScoreRecord;
import com.credo.backend.repository.ScoreRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Set;

@Service
public class ScoreService {

    private static final Set<String> VALID_RISK_BANDS =
            Set.of("LOW", "MODERATE", "HIGH");

    private final MlServiceClient mlServiceClient;
    private final ScoreRepository scoreRepository;

    public ScoreService(
            MlServiceClient mlServiceClient,
            ScoreRepository scoreRepository) {
        this.mlServiceClient = mlServiceClient;
        this.scoreRepository = scoreRepository;
    }

    @Transactional
    public List<ScoreResponse> score(ScoreRequest request) {

        MlServiceResponse response = mlServiceClient.score(request);

        if (response == null || response.results() == null
                || response.results().isEmpty()) {
            throw new IllegalStateException(
                    "Invalid response received from ML service");
        }

        List<ScoreRecord> records = response.results().stream()
                .map(result -> {

                    if (result.customerId() == null
                            || result.customerId().isBlank()
                            || result.credoScore() == null
                            || result.credoScore() < 1
                            || result.credoScore() > 100
                            || result.riskBand() == null
                            || !VALID_RISK_BANDS.contains(
                                    result.riskBand().toUpperCase())
                            || result.predictedOutcome() == null
                            || (result.predictedOutcome() != 0
                                    && result.predictedOutcome() != 1)
                            || result.predictedProbability() == null
                            || !Double.isFinite(
                                    result.predictedProbability())
                            || result.predictedProbability() < 0
                            || result.predictedProbability() > 1) {

                        throw new IllegalStateException(
                                "Invalid scoring result received from ML service");
                    }

                    ScoreRecord record = new ScoreRecord();
                    record.setCustomerId(result.customerId());
                    record.setCredoScore(result.credoScore());
                    record.setRiskBand(result.riskBand().toUpperCase());
                    record.setPredictedOutcome(result.predictedOutcome());
                    record.setPredictedProbability(
                            result.predictedProbability());

                    return record;
                })
                .toList();

        scoreRepository.saveAll(records);

        return records.stream()
                .map(record -> new ScoreResponse(
                        record.getCustomerId(),
                        record.getCredoScore(),
                        record.getRiskBand(),
                        record.getPredictedOutcome(),
                        record.getPredictedProbability()
                ))
                .toList();
    }
}
