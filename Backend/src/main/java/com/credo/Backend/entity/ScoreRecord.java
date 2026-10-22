package com.credo.backend.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "score_records")
public class ScoreRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id", nullable = false, length = 100)
    private String customerId;

    @Column(name = "credo_score")
    private Integer credoScore;

    @Column(name = "risk_band", length = 20)
    private String riskBand;

    @Column(name = "predicted_outcome")
    private Integer predictedOutcome;

    @Column(name = "predicted_probability")
    private Double predictedProbability;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    public ScoreRecord() {
    }

    @PrePersist
    protected void onCreate() {
        if (createdAt == null) {
            createdAt = Instant.now();
        }
    }

    public Long getId() {
        return id;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public Integer getCredoScore() {
        return credoScore;
    }

    public void setCredoScore(Integer credoScore) {
        this.credoScore = credoScore;
    }

    public String getRiskBand() {
        return riskBand;
    }

    public void setRiskBand(String riskBand) {
        this.riskBand = riskBand;
    }

    public Integer getPredictedOutcome() {
        return predictedOutcome;
    }

    public void setPredictedOutcome(Integer predictedOutcome) {
        this.predictedOutcome = predictedOutcome;
    }

    public Double getPredictedProbability() {
        return predictedProbability;
    }

    public void setPredictedProbability(Double predictedProbability) {
        this.predictedProbability = predictedProbability;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}