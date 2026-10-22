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

@Service
public class ScoreService {

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

        if (response == null || response.results() == null) {
            throw new IllegalStateException(
                    "Invalid response received from ML service");
        }

        List<ScoreRecord> records = response.results().stream()
                .map(result -> {
                    ScoreRecord record = new ScoreRecord();
                    record.setCustomerId(result.customerId());
                    record.setCredoScore(result.credoScore());
                    record.setRiskBand(result.riskBand());
                    record.setPredictedOutcome(result.predictedOutcome());
                    record.setPredictedProbability(
                            result.predictedProbability());
                    return record;
                })
                .toList();

        scoreRepository.saveAll(records);

        return response.results().stream()
                .map(result -> new ScoreResponse(
                        result.customerId(),
                        result.credoScore(),
                        result.riskBand(),
                        result.predictedOutcome(),
                        result.predictedProbability()
                ))
                .toList();
    }
}