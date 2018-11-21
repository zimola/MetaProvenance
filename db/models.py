from django.db import models


class Investigation(models.Model):
    pass


class Sample(models.Model):
    """
    Registers a sample taken at a distinct place
    """
    pass


class SampleMetaData(models.Model):
    pass


class BiologicalReplicate(models.Model):
    pass


class BiologicalReplicateMetadata(models.Model):
    pass


class Documents(models.Model):
    pass


class ProtocolParameterDeviation(models.Model):
    pass


class BiologicalReplicatePortal(models.Model):
    pass


class ProtocolStep(models.Model):
    pass


class ProtocolParameter(models.Model):
    pass


class PipelineResult(models.Model):
    pass


class PipelineDeviation(models.Model):
    pass


class ComputationalPipeline(models.Model):
    pass


class PipelineStep(models.Model):
    pass


class PipelineParameter(models.Model):
    pass

