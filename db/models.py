from django.db import models


class Investigation(models.Model):
    """
    Groups of samples, biosamples, and compsamples
    """
    description = models.TextField()


class Sample(models.Model):
    """
    Uniquely identify a single sample (i.e., a physical sample taken at some single time and place)
    """
    name = models.TextField(unique=True)
    investigation = models.ForeignKey('Investigation', on_delete=models.CASCADE)  # fk 2



class SampleMetaData(models.Model):
    """
    Stores arpitrary metadats in key-value pairs
    """
    key = models.TextField()
    value = models.TextField()
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)  # fk 3



class BiologicalReplicate(models.Model):
    """
    A sample resulting from a biological analysis of a collected sample.
    If a poo sample is a sample, the DNA extracted and amplified with primer
    set A is a BiologicalReplicate of that sample

    metadata = BiologicalReplicateMetadata
    protocol = BiologicalReplicateProtocol
    protocol_deviations = ProtocolDeviations
    """
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)  # fk 1
    biological_replicate_protocol = models.OneToOneField('BiologicalReplicateProtocol', on_delete=models.CASCADE)  # fk 5
    pass


class BiologicalReplicateMetadata(models.Model):
    """
    Metadata for the biological sample (PCR primers, replicate #, storage method, etc.)
    """
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE) # fk 14
    pass


class Document(models.Model):  #file
    """
    Store information to locate arbitrary files
    """
    pipeline_result = models.ForeignKey('PipelineResult', on_delete=models.CASCADE)  # fk 10
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE)  # fk 4
    pass


class ProtocolParameterDeviation(models.Model):
    """
    Keep track of when a BiologicalReplicate isn't done exactly as SOP
    """
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE)  # fk 9
    pass


class BiologicalReplicateProtocol(models.Model):
    """
    A list of the steps that the biological sample was processed with
    """
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE)  # fk 6
    pass


class ProtocolStep(models.Model):
    """
    Names and descriptions of the protocol steps and methods, e.g., stepname = 'amplification', method='pcr'
    """
    step_name = models.TextField()
    method = models.TextField()
    description = models.TextField()
    biological_replicate_protocol = models.ManyToManyField('BiologicalReplicateProtocol')  # fk 7
    pass


class ProtocolParameter(models.Model):
    """
    The default parameters for each protocol step
    """
    biological_replicate_protocol = models.ForeignKey('BiologicalReplicateProtocol', on_delete=models.CASCADE)  # fk 8
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
    pipeline_result = models.ForeignKey('PipelineResult', on_delete=models.CASCADE)  # fk 11
    pass


class ComputationalPipeline(models.Model):
    """
    Stores the steps and default parameters for a pipeline
    """
    pipeline_step = models.ManyToManyField('PipelineStep') # fk 12
    pass


class PipelineStep(models.Model):
    """
    Describes a single step in the computational pipeline.
    These can be programatically defined by QIIME's transformations.

    """
    # many to many
    # computational_pipeline = models.ForeignKey('ComputationalPipeline', on_delete=models.CASCADE)  # fk 12

    pass


class PipelineParameter(models.Model):
    """
    The default parameters for each step, for this pipeline
    """
    computational_pipeline = models.ForeignKey('ComputationalPipeline', on_delete=models.CASCADE)  # fk 13
    pass

