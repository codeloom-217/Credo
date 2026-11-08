
package com.credo.backend.controller;

import com.credo.backend.dto.request.ScoreRequest;
import com.credo.backend.dto.response.ScoreResponse;
import com.credo.backend.service.ScoreService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ScoreController.class)
@AutoConfigureMockMvc(addFilters = false)
class ScoreControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ScoreService scoreService;

    @Test
    void shouldReturnScoringResultsForValidRequest() throws Exception {

        when(scoreService.score(any(ScoreRequest.class)))
                .thenReturn(List.of(
                        new ScoreResponse(
                                "CUST001", 75, "LOW", 0, 0.25
                        )
                ));

        String request = """
                {
                    "transactions": [
                        {
                            "customer_id": "CUST001",
                            "transaction_date": "2026-11-08",
                            "transaction_type": "CREDIT",
                            "amount": 1000.0,
                            "balance": 5000.0,
                            "transaction_mode": "UPI",
                            "narration": "salary"
                        }
                    ]
                }
                """;

        mockMvc.perform(post("/v1/score")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(request))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(
                        MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].customerId").value("CUST001"))
                .andExpect(jsonPath("$[0].credoScore").value(75))
                .andExpect(jsonPath("$[0].riskBand").value("LOW"));

        verify(scoreService, times(1)).score(any(ScoreRequest.class));
    }

    @Test
    void shouldRejectEmptyTransactions() throws Exception {

        String request = """
                {
                    "transactions": []
                }
                """;

        mockMvc.perform(post("/v1/score")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(request))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(scoreService);
    }

    @Test
    void shouldRejectBlankCustomerId() throws Exception {

        String request = """
                {
                    "transactions": [
                        {
                            "customer_id": "",
                            "transaction_date": "2026-11-08",
                            "transaction_type": "CREDIT",
                            "amount": 1000.0,
                            "balance": 5000.0,
                            "transaction_mode": "UPI",
                            "narration": "salary"
                        }
                    ]
                }
                """;

        mockMvc.perform(post("/v1/score")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(request))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(scoreService);
    }
}
