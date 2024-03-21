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
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_5', 'ET_Raster_5', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_6', 'ET_Raster_6', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_7', 'ET_Raster_7', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_8', 'ET_Raster_8', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_9', 'ET_Raster_9', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_10', 'ET_Raster_10', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Bc_raster', 'BC_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Cc_raster', 'CC_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster1', 'ET_Raster1', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('P_raster', 'P_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Av_raster', 'AV_Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster2', 'ET_Raster2', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster3', 'ET_Raster3', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Et_raster_4', 'ET_Raster_4', createByDefault=True, defaultValue=''))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(30, model_feedback)
        results = {}
        outputs = {}

        # BC_Buffer
        alg_params = {
            'DISTANCE': 100,
            'INPUT': parameters['bicicletas_compartilhadas'],
            'RINGS': 3,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Bc_buffer'] = processing.run('native:multiringconstantbuffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
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

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # BP_Raster_Process
        alg_params = {
            'BURN': None,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': 'distance',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': outputs['Bp_buffer']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['Bp_raster']
        }
        outputs['Bp_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bp_raster'] = outputs['Bp_raster_process']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

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

        feedback.setCurrentStep(4)
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

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # BC_Raster_Process
        alg_params = {
            'BURN': None,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': None,
            'FIELD': 'distance',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': outputs['Bc_buffer']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': None,
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['Bc_raster']
        }
        outputs['Bc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Bc_raster'] = outputs['Bc_raster_process']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Braços condicionais
        alg_params = {
        }
        outputs['BraosCondicionais'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Buffer ET10
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais10'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt10'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Buffer ET8
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais8'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt8'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Buffer ET9
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais9'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt9'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Buffer ET7
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais7'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt7'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # ET9_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt9']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_9']
        }
        outputs['Et9_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_9'] = outputs['Et9_raster_process']['OUTPUT']

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
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': outputs['BufferP']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['P_raster']
        }
        outputs['P_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['P_raster'] = outputs['P_raster_process']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # ET10_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt10']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_10']
        }
        outputs['Et10_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_10'] = outputs['Et10_raster_process']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # CC_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': outputs['BufferCc']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['Cc_raster']
        }
        outputs['Cc_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cc_raster'] = outputs['Cc_raster_process']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Buffer ET1
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes__terminais1'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt1'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Buffer ET2
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais2'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt2'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # AV_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': parameters['areas_verdes'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['Av_raster']
        }
        outputs['Av_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Av_raster'] = outputs['Av_raster_process']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Buffer ET3
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais3'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt3'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # ET1_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt1']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster1']
        }
        outputs['Et1_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster1'] = outputs['Et1_raster_process']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Buffer ET4
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais4'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt4'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # ET2_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 10,
            'INIT': None,
            'INPUT': outputs['BufferEt2']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 10,
            'OUTPUT': parameters['Et_raster2']
        }
        outputs['Et2_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster2'] = outputs['Et2_raster_process']['OUTPUT']

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Buffer ET6
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais6'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt6'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # ET6_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt6']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_6']
        }
        outputs['Et6_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_6'] = outputs['Et6_raster_process']['OUTPUT']

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # ET4_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt4']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_4']
        }
        outputs['Et4_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_4'] = outputs['Et4_raster_process']['OUTPUT']

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # ET8_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt8']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_8']
        }
        outputs['Et8_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_8'] = outputs['Et8_raster_process']['OUTPUT']

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Buffer ET5
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['estacoes_terminais5'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 1,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferEt5'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # ET3_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt3']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster3']
        }
        outputs['Et3_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster3'] = outputs['Et3_raster_process']['OUTPUT']

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # ET7_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt7']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_7']
        }
        outputs['Et7_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_7'] = outputs['Et7_raster_process']['OUTPUT']

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # ET5_Raster_Process
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': None,
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 50,
            'INIT': None,
            'INPUT': outputs['BufferEt5']['OUTPUT'],
            'INVERT': False,
            'NODATA': None,
            'OPTIONS': '',
            'UNITS': 1,  # Unidades georreferenciados
            'USE_Z': False,
            'WIDTH': 50,
            'OUTPUT': parameters['Et_raster_5']
        }
        outputs['Et5_raster_process'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Et_raster_5'] = outputs['Et5_raster_process']['OUTPUT']
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
