
package com.credo.backend.service;

import com.credo.backend.client.MlServiceClient;
import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.request.TransactionRequest;
import com.credo.backend.dto.response.MlServiceResponse;
import com.credo.backend.entity.ScoreRecord;
import com.credo.backend.repository.ScoreRepository;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ScoreServiceTest {

    @Mock
    private MlServiceClient mlServiceClient;

    @Mock
    private ScoreRepository scoreRepository;

    @InjectMocks
    private ScoreService scoreService;

    @Test
    void shouldSaveAndReturnValidScoringResults() {

        ScoreRequest request = createRequest("CUST001");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST001", 75, "LOW", 0, 0.25))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        var results = scoreService.score(request);

        assertEquals(1, results.size());
        assertEquals("CUST001", results.get(0).customerId());
        assertEquals(75, results.get(0).credoScore());
        assertEquals("LOW", results.get(0).riskBand());

        verify(scoreRepository).saveAll(anyList());
    }

    @Test
    void shouldRejectNullMlResponse() {

        ScoreRequest request = createRequest("CUST001");

        when(mlServiceClient.score(request)).thenReturn(null);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectEmptyMlResults() {

        ScoreRequest request = createRequest("CUST001");

        when(mlServiceClient.score(request))
                .thenReturn(new MlServiceResponse("success", List.of()));

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectInvalidCredoScore() {

        ScoreRequest request = createRequest("CUST001");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST001", 110, "LOW", 0, 0.25))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectInvalidRiskBand() {

        ScoreRequest request = createRequest("CUST001");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST001", 75, "UNKNOWN", 0, 0.25))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectInvalidProbability() {

        ScoreRequest request = createRequest("CUST001");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST001", 75, "LOW", 0, Double.NaN))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectDuplicateCustomerResults() {

        ScoreRequest request = createRequest("CUST001", "CUST002");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(
                        createResult("CUST001", 75, "LOW", 0, 0.25),
                        createResult("CUST001", 65, "MODERATE", 1, 0.65)
                )
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectMissingCustomerResults() {

        ScoreRequest request = createRequest("CUST001", "CUST002");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST001", 75, "LOW", 0, 0.25))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    @Test
    void shouldRejectUnexpectedCustomerIds() {

        ScoreRequest request = createRequest("CUST001");

        MlServiceResponse response = new MlServiceResponse(
                "success",
                List.of(createResult("CUST999", 75, "LOW", 0, 0.25))
        );

        when(mlServiceClient.score(request)).thenReturn(response);

        assertThrows(
                IllegalStateException.class,
                () -> scoreService.score(request)
        );

        verify(scoreRepository, never()).saveAll(anyList());
    }

    private ScoreRequest createRequest(String... customerIds) {

        List<TransactionRequest> transactions =
                java.util.Arrays.stream(customerIds)
                        .map(id -> new TransactionRequest(
                                id,
                                "2026-11-07",
                                "CREDIT",
                                100.0,
                                200.0,
                                "UPI",
                                "salary"
                        ))
                        .toList();

        return new ScoreRequest(transactions);
    }

    private MlServiceResponse.Result createResult(
            String customerId,
            Integer score,
            String riskBand,
            Integer outcome,
            Double probability) {

        return new MlServiceResponse.Result(
                customerId,
                score,
                riskBand,
                outcome,
                probability
        );
    }
}
