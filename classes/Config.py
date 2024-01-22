import numpy as np
import cv2

class Config:
    
    def dBm2Lin(dBm):
        Lin = pow(10,-3) * pow(10,(dBm/10))
        return Lin
    
    #Pb = dBm2Lin(30);
    Pb = 10**(30/10)
    #Pu = dBm2Lin(10);
    Pu = 10**(10/10)
    sigma = -94;
    FUL = 1800;
    FDL = 1800;
    NW = 30;
    b = 2;
    M = 15;
    m = 0.7;
    phi = 30;
    Y = 10;
    gamma = 0.5;
    w = 0.98;
    sigSquareGA_i = 0.151;
    dzero = 5;
    #fc = 28
    fc = 28 * 10**9;
    c = 3 * 10**8;
    wlLoS = 2;
    wlNLoS = 2.4;
    miSigmaLoS = 5.3;
    miSigmaNLoS = 5.27;
    GA = 11;
    phiDelay = 10;
    phiQuality = 0.8;
    sigmaSquare_i = 0.193;
    A = 50;
    T = 5;
    lambda_ = 0.005;
    L = 3;
    v = 2;
    sigmaSquareB = 0.05;
    '''
    BaseStation = {[-500, -500],
                   [-500, 500],
                   [0.0, 0.0],
                   [500, 500],
                   [500, -500]};
    '''
    '''
    us = 20;
    bs = 5;
    obj = 2;
    ti = 13;
    '''
    #####################################
    us = 300; # numero de usuários
    bs = 5; # numero de base stations
    obj = 1; # numero de objetos
    ti = 10; # quantidade de estampas de tempo
    V = 90; # limite de usuários bor BS no Downlink
    
    prefix_in = ''
    prefix_in = 'instances/' + str(us) + '/'
    
    prefix_out = ''
    #prefix_out = 'outputs/OP/' + str(us) + '_'
    
    users_file = prefix_in + 'users.json'
    bs_file = prefix_in + 'base_stations.json'
    decisions_file = prefix_in + 'BIP_for_all_combinations.json'
    results_file = prefix_out + 'results.json'
    #####################################
    #p_2 = dBm2Lin(-105)
    p_2 = 10**(-105/10)

    #VR_Frame = cv2.imread("3DShootGame-Frame.jpg")
    # convert to RGB
    #VR_Frame = cv2.cvtColor(VR_Frame, cv2.COLOR_BGR2RGB)
    
    VR_Frame = np.random.randint(256, size=(64, 48, 3))
    BaseResolution = len(VR_Frame) * len(VR_Frame[0])
    
    BaseResolutionBitsPerPixel = 24;
    
    
    LightSpeed = 299792458


