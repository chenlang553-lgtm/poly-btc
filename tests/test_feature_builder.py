from pipeline.build_features import build_features


def test_feature_builder_has_z(sample_snapshots) -> None:
    df = build_features(sample_snapshots)
    assert "z" in df.columns
    assert "weak_theta_gap" in df.columns
