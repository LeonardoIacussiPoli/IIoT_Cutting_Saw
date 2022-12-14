from pre_processing_core import *

class preProcessingData(object):
    shift_samples = None
    input_buffer_size = None
    ism330dhcx_odr = None
    axis = None
    triangular_filters_scale = None
    signal_windowing = None
    bin = None

        
def pre_processing_init():
    
    pre_processing_data = preProcessingData()

    #data preparation
    pre_processing_data.shift_samples = 56

    #sensors
    pre_processing_data.input_buffer_size = 256
    pre_processing_data.ism330dhcx_odr = float("1666.0f"[:-1])
    
    #axis_selection
    pre_processing_data.axis = "Y".lower()

    #mfcc
    pre_processing_data.triangular_filters_scale = "TRIANGULAR_FILTERS_SCALE_HZ"
    pre_processing_data.signal_windowing = "RECTANGULAR"
    pre_processing_data.bin = triangular_filters_init(pre_processing_data.input_buffer_size, pre_processing_data.ism330dhcx_odr, pre_processing_data.triangular_filters_scale)

    return pre_processing_data


def pre_processing_process(data_in_df , pre_processing_data):

    # data slicing 
    dataset_cols_size = 128  # HANDLEBARS!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    dataset_rows_size=int(np.floor((len(data_in_df)-pre_processing_data.input_buffer_size)/pre_processing_data.shift_samples)+1)    # dataset initialization
    X = np.zeros((dataset_rows_size,dataset_cols_size))

    for row in range(dataset_rows_size):
        sub_df = data_in_df.iloc[row*pre_processing_data.shift_samples : row*pre_processing_data.shift_samples + pre_processing_data.input_buffer_size, :]

        '''
        PRE-PROCESSING
        '''

        # axis selection
        data_0 = axis_selection(sub_df, pre_processing_data.axis)

        # mean removal
        data_1 = mean_removal(data_0)

        # mfcc
        #data_out = mfcc_(data_1, pre_processing_data.bin, pre_processing_data.signal_windowing)
        data_out = fft_(data_1, pre_processing_data.signal_windowing)

        '''
        END-PREPROCESSING
        '''

        # dataset
        X[row,:] = data_out

    return X

