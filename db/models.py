from django.db import models


class Investigation(models.Model):
    """
    Groups of samples, biosamples, and compsamples
    """
    pass


class Sample(models.Model):
    """
    Registers a sample taken at a distinct place
    """
    metadata = models.ForeignKey(SampleMetaData, on_delete=models.CASCADE)
    pass


class SampleMetaData(models.Model):
    """
    Stores arpitrary metadats in key-value pairs
    """
    key = models.TextField()
    value = models.TextField()
    pass


class BiologicalReplicate(models.Model):
    """
    A sample resulting from a biological analysis of a collected sample.
    If a poo sample is a sample, the DNA extracted and amplified with primer
    set A is a BiologicalReplicate of that sample
    """
    pass


class BiologicalReplicateMetadata(models.Model):
    """
    Metadata for the biological sample (PCR primers, replicate #, storage method, etc.)
    """
    pass


class Document(models.Model):
    """
    Store information to locate arbitrary files
    """
    pass


class ProtocolParameterDeviation(models.Model):
    """
    Keep track of when a BiologicalReplicate isn't done exactly as SOP
    """
    pass


class BiologicalReplicateProtocol(models.Model):
    """
    A list of the steps that the biological sample was processed with
    """
    pass


class ProtocolStep(models.Model):
    """
    Names and descriptions of the protocol steps and methods, e.g., stepname = 'amplification', method='pcr'
    """
    pass


class ProtocolParameter(models.Model):
    """
    The default parameters for each protocol step
    """
    pass


class PipelineResult(models.Model):
    """
    Some kind of result from a ComputationalPipeline
    """
    pass


class PipelineDeviation(models.Model):
    """
    Keep track of when an object's provenance involves deviations in the listed SOP
    """
    pass


class ComputationalPipeline(models.Model):
    """
    Stores the steps and default parameters for a pipeline
    """
    pass


class PipelineStep(models.Model):
    """
    Describes a single step in the computational pipeline.
    These can be programatically defined by QIIME's transformations.
    """
    pass


class PipelineParameter(models.Model):
    """
    The default parameters for each step, for this pipeline
    """
    pass

