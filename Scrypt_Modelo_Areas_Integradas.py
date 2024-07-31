"""
Model exported as python.
Name : Areas Integradas
Group : 
With QGIS : 32401
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
        self.addParameter(QgsProcessingParameterRasterDestination('Bc_raster', 'BC_Raster', createByDefault=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterDestination('Bp_raster', 'BP_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Cc_raster', 'CC_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('P_raster', 'P_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Av_raster', 'AV_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster', 'ET_Raster', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(22, model_feedback)
        results = {}
        outputs = {}

        # Braços condicionais
        alg_params = {
        }
        outputs['BraosCondicionais'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # BP_Buffer
        alg_params = {
            'DISTANCE': 1,
            'INPUT': parameters['bicicletarios_e_paraciclos'],
            'RINGS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bp_buffer'] = processing.run('native:multiringconstantbuffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Buffer P
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 50,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['paradas'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferP'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Buffer AV
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 50,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['areas_verdes'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferAv'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # BC_Buffer
        alg_params = {
            'DISTANCE': 1,
            'INPUT': parameters['bicicletas_compartilhadas'],
            'RINGS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bc_buffer'] = processing.run('native:multiringconstantbuffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
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
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bp_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Buffer CC
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 50,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['ciclovias_e_ciclofaixas'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferCc'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
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
            'INPUT': outputs['BufferAv']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Av_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Estacoes_Terminais_Mesclado
        alg_params = {
            'CRS': 'ProjectCrs',
            'LAYERS': [parameters['estacoes__terminais1'],parameters['estacoes_terminais2'],parameters['estacoes_terminais3'],parameters['estacoes_terminais4'],parameters['estacoes_terminais10'],parameters['estacoes_terminais5'],parameters['estacoes_terminais6'],parameters['estacoes_terminais7'],parameters['estacoes_terminais8'],parameters['estacoes_terminais9']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Estacoes_terminais_mesclado'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Buffer ET
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 50,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': outputs['Estacoes_terminais_mesclado']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
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
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['P_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Proximidade (distância raster) BP
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTRA': '',
            'INPUT': outputs['Bp_raster_process']['OUTPUT'],
            'MAX_DISTANCE': 300,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,  # Coordenadas georeferenciadas
            'VALUES': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximidadeDistnciaRasterBp'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela P
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['P_raster_process']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','0','1','1','1','5'],
            'OUTPUT': parameters['P_raster']
        }
        outputs['ReclassificarPorTabelaP'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['P_raster'] = outputs['ReclassificarPorTabelaP']['OUTPUT']

        feedback.setCurrentStep(13)
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
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela BP
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['ProximidadeDistnciaRasterBp']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','100','5','100','200','3','200','300','1'],
            'OUTPUT': parameters['Bp_raster']
        }
        outputs['ReclassificarPorTabelaBp'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bp_raster'] = outputs['ReclassificarPorTabelaBp']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela AV
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['Av_raster_process']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','0','1','1','1','5'],
            'OUTPUT': parameters['Av_raster']
        }
        outputs['ReclassificarPorTabelaAv'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Av_raster'] = outputs['ReclassificarPorTabelaAv']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # ET_Raster_Process
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
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Et_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
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
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Cc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela ET
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['Et_raster_process']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','0','1','1','1','5'],
            'OUTPUT': parameters['Et_raster']
        }
        outputs['ReclassificarPorTabelaEt'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster'] = outputs['ReclassificarPorTabelaEt']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela CC
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['Cc_raster_process']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','0','1','1','1','5'],
            'OUTPUT': parameters['Cc_raster']
        }
        outputs['ReclassificarPorTabelaCc'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cc_raster'] = outputs['ReclassificarPorTabelaCc']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Proximidade (distância raster)BC
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTRA': '',
            'INPUT': outputs['Bc_raster_process']['OUTPUT'],
            'MAX_DISTANCE': 300,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,  # Coordenadas georeferenciadas
            'VALUES': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximidadeDistnciaRasterbc'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Reclassificar por tabela BC
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'INPUT_RASTER': outputs['ProximidadeDistnciaRasterbc']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,  # min < valor <= max
            'RASTER_BAND': 1,
            'TABLE': ['0','100','5','100','200','3','200','300','1'],
            'OUTPUT': parameters['Bc_raster']
        }
        outputs['ReclassificarPorTabelaBc'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bc_raster'] = outputs['ReclassificarPorTabelaBc']['OUTPUT']
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
