"""Verifies the graphs that are provided for the output of the first stage of
the experiment.

Input: Experiment configuration.
    SubInput: Run configuration within an experiment.
        Stage 1: The networkx graphs that will be propagated.
        Stage 2: The propagated networkx graphs (at least one per timestep).
        Stage 3: Visaualisation of the networkx graphs over time.
        Stage 4: Post-processed performance data of algorithm and adaptation
        mechanism.
"""
from typeguard import typechecked


# pylint: disable=W0613
@typechecked
def verify_stage_3_graphs(
    experiment_config: dict, run_config: dict, graphs_stage_3: dict
) -> None:
    """Verifies the generated graphs are compliant and complete for the
    specified run configuration.

    An experiment may consist of multiple runs.
    """
    # TODO: Verify run_config is valid "subset" of experiment config.

    # Compute which graphs are expected, based on run config.

    # Verify the graphs that are required for the run_config are generated.

    # TODO: verify the properties required by the run config are in the graphs.
