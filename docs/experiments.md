# Running experiments

The main class is `experimaestro.experiment`


::: experimaestro.experiment

When using the command line interface to run experiment, the main object
of interaction is the `ExperimentHelper`:

::: experimaestro.experiments.cli.ExperimentHelper

## Experiment services

::: experimaestro.scheduler.services.Service
::: experimaestro.scheduler.services.WebService
::: experimaestro.scheduler.services.ServiceListener


## Experiment configuration

The module `experimaestro.experiments` contain code factorizing boilerplate for
launching experiments. It allows to setup the experimental environment and
read ``YAML`` configuration files to setup some experimental parameters.

This can be extended to support more specific experiment helpers (see e.g.
experimaestro-ir for an example).

`ConfigurationBase` should be the parent class of any configuration.

::: experimaestro.experiments.ConfigurationBase

### Example

An `experiment.py` file:

```py3
    from experimaestro.experiments import ExperimentHelper, configuration, ConfigurationBase

    @configuration
    class Configuration(ConfigurationBase):
        #: Default learning rate
        learning_rate: float = 1e-3

    def run(
        helper: ExperimentHelper, cfg: Configuration
    ):
        # Experimental code
        ...
```

With `full.yaml` located in the same folder as `experiment.py`

```yaml
    file: experiment
    learning_rate: 1e-4
```

The experiment can be started with

```sh
    experimaestro run-experiment --run-mode normal full.yaml
```

### Other options

The Python path can be set by the configuration file, and module be used instead
of a file:

```yaml
    # Module name containing the "run" function
    module: first_stage.experiment

    # Python paths relative to the directory containing this YAML file
    pythonpath:
        - ../src
```

### Common handling

::: experimaestro.experiments.cli
