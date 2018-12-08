from django.db import models

class Investigation(models.Model):
    """
    Groups of samples, biosamples, and compsamples
    """
    name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    description = models.TextField()


class Sample(models.Model):
    """
    Uniquely identify a single sample (i.e., a physical sample taken at some single time and place)
    """
    name = models.CharField(max_length=255,unique=True)
    investigation = models.ForeignKey('Investigation', on_delete=models.CASCADE)  # fk 2


class SampleMetadata(models.Model):
    """
    Stores arbitrary metadata in key-value pairs
    """
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
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
    name = models.CharField(max_length=255,unique=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)  # fk 1
    sequence_file = models.ManyToManyField('Document') # store the location of the sequence file(s)
    biological_replicate_protocol = models.ForeignKey('BiologicalReplicateProtocol', on_delete=models.CASCADE)  # fk 5


class BiologicalReplicateMetadata(models.Model):
    """
    Metadata for the biological sample (PCR primers, replicate #, storage method, etc.)
    Basically anything that could change between a Sample and a BiologicalReplicate
    goes in here
    """
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE) # fk 14


class Document(models.Model):  #file
    """
    Store information to locate arbitrary files
    """
    md5_hash = models.CharField(max_length=255)
    document = models.FileField()
    #We can get size and location through the FileSystem manager in Django


class ProtocolParameterDeviation(models.Model):
    """
    Keep track of when a BiologicalReplicate isn't done exactly as SOP
    """
    # Identifies which replicate is deviating
    biological_replicate = models.ForeignKey('BiologicalReplicate', on_delete=models.CASCADE)  # fk 9
    # Stores the default
    protocol_step = models.ForeignKey('ProtocolStep', on_delete=models.CASCADE) # fk ??
    # Comment expanding on what the deviation was
    description = models.TextField()
    # Stores the deviation from the default
    value = models.TextField()


class BiologicalReplicateProtocol(models.Model):
    """
    A list of the steps that the biological sample was processed with
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    #citation = models.TextField() # should we include citations, or just have that in description?


class ProtocolStep(models.Model):
    """
    Names and descriptions of the protocol steps and methods, e.g., stepname = 'amplification', method='pcr'
    """
    step_name = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    biological_replicate_protocol = models.ManyToManyField('BiologicalReplicateProtocol')  # fk 7


class ProtocolStepParameter(models.Model):
    """
    The default parameters for each protocol step
    """
    biological_replicate = models.ForeignKey('ProtocolStep', 
                                             on_delete=models.CASCADE) # fk ??
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    description = models.TextField()


class PipelineResult(models.Model):
    """
    Some kind of result from a ComputationalPipeline
    """
    document = models.ManyToManyField('Document')
    computational_pipeline = models.ForeignKey('ComputationalPipeline', on_delete=models.CASCADE)
    pipeline_step = models.ForeignKey('PipelineStep', on_delete=models.CASCADE)


class PipelineDeviation(models.Model):
    """
    Keep track of when an object's provenance involves deviations in the listed SOP
    """
    pipeline_result = models.ForeignKey('PipelineResult', on_delete=models.CASCADE)  # fk 11
    pipeline_parameter = models.ForeignKey('PipelineParameter', on_delete=models.CASCADE) # fk ??
    value = models.CharField(max_length=255)


class ComputationalPipeline(models.Model):
    """
    Stores the steps and default parameters for a pipeline
    """
    pipeline_step = models.ManyToManyField('PipelineStep') # fk 12


class PipelineStep(models.Model):
    """
    Describes a single step in the computational pipeline.
    These can be programatically defined by QIIME's transformations.

    """
    # many to many
    name = models.CharField(max_length=255)


class PipelineParameter(models.Model):
    """
    The default parameters for each step, for this pipeline
    """
    computational_pipeline = models.ForeignKey('ComputationalPipeline', on_delete=models.CASCADE) # fk ??
    pipeline_step = models.ForeignKey('PipelineStep', on_delete=models.CASCADE)  # fk 13
    value = models.CharField(max_length=255)
    key = models.CharField(max_length=255)

