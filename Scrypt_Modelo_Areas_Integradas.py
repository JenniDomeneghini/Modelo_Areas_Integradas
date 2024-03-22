"""
Model exported as python.
Name : Areas Integradas
Group : 
With QGIS : 33403
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class AreasIntegradas(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('bicicletarios_e_paraciclos', 'Bicicletarios e Paraciclos', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('bicicletas_compartilhadas', 'Bicicletas Compartilhadas', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('ciclovias_e_ciclofaixas', 'Ciclovias e Ciclofaixas', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('areas_verdes', 'Areas_Verdes', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('paradas', 'Paradas', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes__terminais1', 'Estacoes_ Terminais1', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais2', 'Estacoes_Terminais2', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais3', 'Estacoes_Terminais3', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais4', 'Estacoes_Terminais4', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais5', 'Estacoes_Terminais5', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais6', 'Estacoes_Terminais6', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais7', 'Estacoes_Terminais7', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais8', 'Estacoes_Terminais8', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais9', 'Estacoes_Terminais9', optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('estacoes_terminais10', 'Estacoes_Terminais10', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Bp_raster', 'BP_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Bc_raster', 'BC_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Cc_raster', 'CC_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster', 'ET_Raster', createByDefault=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterDestination('P_raster', 'P_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Av_raster', 'AV_Raster', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(13, model_feedback)
        results = {}
        outputs = {}

        # Buffer CC
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['ciclovias_e_ciclofaixas'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferCc'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # CC_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': outputs['BufferCc']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['Cc_raster']
        }
        outputs['Cc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cc_raster'] = outputs['Cc_raster_process']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Estacoes_Terminais_Mesclado
        alg_params = {
            'CRS': 'ProjectCrs',
            'LAYERS': [parameters['estacoes__terminais1'],parameters['estacoes_terminais2'],parameters['estacoes_terminais3'],parameters['estacoes_terminais4'],parameters['estacoes_terminais10'],parameters['estacoes_terminais5'],parameters['estacoes_terminais6'],parameters['estacoes_terminais7'],parameters['estacoes_terminais8'],parameters['estacoes_terminais9']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Estacoes_terminais_mesclado'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Buffer P
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['paradas'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferP'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # BC_Buffer
        alg_params = {
            'DISTANCE': 100,
            'INPUT': parameters['bicicletas_compartilhadas'],
            'RINGS': 3,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bc_buffer'] = processing.run('native:multiringconstantbuffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Braços condicionais
        alg_params = {
        }
        outputs['BraosCondicionais'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # BP_Buffer
        alg_params = {
            'DISTANCE': 100,
            'INPUT': parameters['bicicletarios_e_paraciclos'],
            'RINGS': 3,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bp_buffer'] = processing.run('native:multiringconstantbuffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # BP_Raster_Process
        alg_params = {
            'BURN': None,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': 'distance',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': outputs['Bp_buffer']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['Bp_raster']
        }
        outputs['Bp_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bp_raster'] = outputs['Bp_raster_process']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # P_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': outputs['BufferP']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['P_raster']
        }
        outputs['P_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['P_raster'] = outputs['P_raster_process']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Buffer ET
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['Estacoes_terminais_mesclado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # BC_Raster_Process
        alg_params = {
            'BURN': None,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': 'distance',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': outputs['Bc_buffer']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['Bc_raster']
        }
        outputs['Bc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bc_raster'] = outputs['Bc_raster_process']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # AV_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': parameters['areas_verdes'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['Av_raster']
        }
        outputs['Av_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Av_raster'] = outputs['Av_raster_process']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # P_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 1,
            'INIT': None,
            'INPUT': outputs['BufferEt']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': parameters['Et_raster']
        }
        outputs['P_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster'] = outputs['P_raster_process']['OUTPUT']
        return results

    def name(self):
        return 'Areas Integradas'

    def displayName(self):
        return 'Areas Integradas'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return AreasIntegradas()
