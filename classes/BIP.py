from classes.Config import Config
import random
import math
import numpy as np
import commpy.modulation as mod
import cv2
import json


config = Config()
los_nlos_file = 'los_or_nlos.json'

class BIP:
    l_it = None
    m_it = None
    
    def __init__(self):
        self.l_it = self.generateImportancePixelVector()
        self.m_it =  self.simulateTransmission()
        #print(self.l_it, self.l_it.shape)
        #print(self.m_it, self.m_it.shape)
    
    '''
    Calculate Break in Presence, of user i in association to base station j at the time t
    '''
    def calculateDataRate(self, user, bs_ul, bs_dl, time, users):
            return (self.calculateUploadDataRate(user, bs_ul, time, users),
                    self.calculateDownloadDataRate(user, bs_dl, time, users))
            
    def calculateUploadDataRate(self, user, base_station, time, users):

        skU = self.sumNoise(user, base_station, time, users);

        dij = math.sqrt(pow((base_station.x - user.x[time]),2) + pow((base_station.y - user.y[time]),2))
        
        gij = self.getRayleighChannelGain(dij);
        
        ijtUL = config.FUL * math.log2(1 + ((config.Pu * gij * pow(dij, -config.b))/skU))
        
        return ijtUL
        
    def calculateDownloadDataRate(self, user, base_station, time, users):
        Gijt = self.getAntennaGain(user, base_station, time)
        #biXijt = self.getAutoBlockage(user, base_station, time)
        hijtLoS = self.getPathLossForLoS(user, base_station, time)
        hijtNLoS = self.getPathLossForNLoS(user, base_station, time)
        #print(hijtLoS, hijtNLoS)
        #nijt = self.getAmountBlockage(user, base_station, time, users)

        with open(los_nlos_file) as json_file:
            data = json.load(json_file)
            
        los_nlos = data['t' + str(time) + '_u' + str(user.id_) + '_bs' + str(base_station.id_)]
        
        '''
        if(biXijt + nijt == 0):
            ijtDL = config.FDL * math.log2(1 + ((config.Pb * Gijt) / pow(10, (hijtLoS / 10)) * config.p_2))
        elif(biXijt + nijt > 0):
            ijtDL = config.FDL * math.log2(1 + ((config.Pb * Gijt) / pow(10, (hijtNLoS / 10)) * config.p_2))
        '''

        if(los_nlos['visibility'] == 'LoS'):
            ijtDL = config.FDL * math.log2(1 + ((config.Pb * Gijt) / (pow(10, (hijtLoS / 10)) * config.p_2)))
        elif(los_nlos['visibility'] == 'NLoS'):
            ijtDL = config.FDL * math.log2(1 + ((config.Pb * Gijt) / (pow(10, (hijtNLoS / 10)) * config.p_2)))

        return ijtDL
 
    def sumNoise(self, user, base_station, time, users):
        sum = 0;

        for i in range(1, config.us + 1):
            user2 = users[i];

            if(user.id_ == user2.id_):
                continue;     

            dkj = math.sqrt(pow((user2.x[time] - base_station.x),2) + pow((user2.y[time] - base_station.y),2))
            #print(user2.x[time], user.x[time], user2.y[time], user.y[time])
            gkj = self.getRayleighChannelGain(dkj)

            sum = sum + config.Pu * gkj * pow(dkj, -config.b)

        sum = sum + config.p_2
        
        return sum

        
    def getRayleighChannelGain(self, d):
        exp_param = (1-math.pi/4)/(pow(d, (-config.b)))
        exp_mu = 1/exp_param

        gain = np.random.exponential(scale=exp_mu)

        return gain

    
    def getAntennaGain(self, user, base_station, time):     
        varphi = math.pi/2*(1-np.sign(user.x[time]-base_station.x)) + math.atan((user.y[time]-base_station.y)/user.x[time]-base_station.x)

        #To ensure a positive angle (in rad)
        if(varphi < 0):
            varphi = (math.pi/2-abs(varphi)) + math.pi/2 + math.pi

        varphi = varphi*180/math.pi #convert to degree
        theta= 45                   # boresight direction (in degree) - antenna direction (arbitrarily defined)
        Q= pow(10, (18/10))         # antenna gain of the mainlobe (Prof. Flavio's orientation)
        q= pow(10, (-2/10))         # antenna gain of the sidelobe (Prof. Flavio's orientation)

        #Equação (2) do artigo
        if (abs(varphi - theta) > config.phi/2):
            gain=q
        else:
            gain=Q
        
        return gain

    '''
    def getAutoBlockage(obj, user, base_station, time):

        varphi = math.pi/2*(1-np.sign(user.x[time]-base_station.x)) + math.atan((user.y[time]-base_station.y)/user.x[time]-base_station.x)

        #To ensure a positive angle (in rad)
        if(varphi < 0):
            varphi=(math.pi/2-abs(varphi)) + math.pi/2 + math.pi

        varphi = varphi*180/math.pi #convert to degree

        if(varphi - user.orientation[time] <= config.v):
            bi_Xijt = 1
        else:
            bi_Xijt = 0
        
        return bi_Xijt
    '''
            
    def getPathLossForLoS(self, user, base_station, time):
                
        fspl = 20 * math.log10((config.dzero * config.fc * 4 * math.pi) / config.LightSpeed)

        dij = math.sqrt(pow((base_station.x - user.x[time]),2) + pow((base_station.y - user.y[time]),2))

        hijt_LoS = 10 * config.wlLoS * math.log10(dij) + fspl + config.miSigmaLoS        
        
        '''        
        d3d = np.linalg.norm(
            np.array([base_station.x, base_station.y, base_station.height])
            -np.array([user.x[time], user.y[time], user.height[time]])
            )
        
        dBP = (4 * base_station.height*user.height[time]*config.fc)/config.LightSpeed
        
        hijt_LoS = 32.4 + (40 * math.log10(d3d)) \
                + (20 * math.log10(config.fc)) \
                - 9.5 * math.log10(pow(dBP, 2) \
                + pow(base_station.height - user.height[time], 2))        
        '''

        return hijt_LoS

    def getPathLossForNLoS(self, user, base_station, time):
        
        fspl = 20 * math.log10((config.dzero * config.fc * 4 * math.pi) / config.LightSpeed)

        dij = math.sqrt(pow((base_station.x - user.x[time]),2) + pow((base_station.y - user.y[time]),2))

        hijt_NLoS = 10 * config.wlNLoS * math.log10(dij) + fspl + config.miSigmaNLoS                
        
        '''
        d3d = np.linalg.norm(np.array([base_station.x, base_station.y, base_station.height])-np.array([user.x[time], user.y[time], user.height[time]]))
        hijt_NLoS = (35.3 * math.log10(d3d)) + 22.4 + (21.3 * math.log10(config.fc)) - (0.3 * (user.height[time] - 1.5))        
        '''

        return hijt_NLoS
        
    '''    
    def getAmountBlockage(self, user, base_station, time, users):
        nijt = 0;

        for i in range(1, config.us+1):
            user2 = users[i]

            if(user.id_, user2.id_):
                continue

            if(self.existBlockage(user, base_station, user2)):
                nijt = nijt + 1
                
        return nijt
    
    
    def existBlockage(self, user, baseStation, user2):
        Limit = 100 * np.spacing(max([abs(x) for x in [user.x,user.y,baseStation.x,baseStation.y,user2.x,user2.y]]))
        if user.x != base_station.x:
            m = (base_station.y-user.y) / (base_station.x-user.x)
            yus2 = m*user2.x + user.y - m*user.x
            R = (abs(user2.y - yus2) < 100 * Limit)
        else:
            R = (user2.x < Limit)
        
        return R
    '''
    
    def calculateBipByTransmission(self, user, bs_ul, bs_dl, time, users):
        timeUlTransmission = 0
        
        timeDlTransmission = 0

        c_ijtUL, c_ijtDL = self.calculateDataRate(user, bs_ul, bs_dl, time, users)

        timeUlTransmission = config.A / c_ijtUL
        timeDlTransmission = self.l_it.sum() / c_ijtDL

        delay = timeUlTransmission + timeDlTransmission > config.phiDelay

        quality = np.dot(self.l_it, self.m_it.T) / config.BaseResolution < config.phiQuality

        w_it = delay or quality
        
        return w_it*1

    
    
    def calculateBipTotal(self, user, bs_ul, bs_dl, time, users):

        w_it = self.calculateBipByTransmission(user, bs_ul, bs_dl, time, users)

        GA_wit = config.GA * w_it

        e_i = math.sqrt(config.sigmaSquare_i)*np.random.randn()
        e_ga_i = math.sqrt(config.sigSquareGA_i)*np.random.randn()
        e_B = math.sqrt(config.sigmaSquareB)*np.random.randn()

        sum = config.GA + w_it + GA_wit + e_i + e_ga_i + e_B

        return sum

    
    def generateImportancePixelVector(self):
        image = config.VR_Frame

        # reshape the image to a 2D array of pixels and 3 color values (RGB)
        pixel_values = image.reshape((-1, 3))
        # convert to float
        pixel_values = np.float32(pixel_values)
        # define stopping criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        # number of clusters (K)
        k = 6
        _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        # convert back to 8 bit values
        centers = np.uint8(centers)
        # flatten the labels array
        labels = labels.flatten()
        # convert all pixels to the color of the centroids
        segmented_image = centers[labels.flatten()]
        # reshape back to the original image dimension
        segmented_image = segmented_image.reshape(image.shape)

        return self.weightedByNormalization(image, segmented_image)
        
        
    def weightedByNormalization(self, RGBO, RGBC):
        maxRed   = RGBO[:,:,0].max()
        minRed   = RGBO[:,:,0].min()
        maxGreen = RGBO[:,:,1].max()
        minGreen = RGBO[:,:,1].min()
        maxBlue  = RGBO[:,:,2].max()
        minBlue  = RGBO[:,:,2].min()

        RNormalized = (RGBC[:,:,0] - minRed) / (maxRed - minRed)
        GNormalized = (RGBC[:,:,1] - minGreen) / (maxGreen - minGreen)
        BNormalized = (RGBC[:,:,2] - minBlue) / (maxBlue - minBlue)

        return np.concatenate((RNormalized.flatten(), GNormalized.flatten(), BNormalized.flatten()))


    def simulateTransmission(self):
        bitsToTransmitte = rgb_matrix_to_bits(config.VR_Frame)        
        
        modulation = mod.QAMModem(64)
        y = modulation.modulate(bitsToTransmitte)
        M=64
        N=len(bitsToTransmitte)
        k=math.log2(M)
        snr=10
        limiteErro=0.1
        m = np.mean(pow(np.abs(y),2))/k
        sigma = math.sqrt(m/(2*snr))
        
        #%noise
        w=sigma*(np.random.randn(int(N/k),1)+1j*np.random.randn(int(N/k),1))

        #%Rayleigh Channel
        H=(1/math.sqrt(2))*(np.random.randn(int(N/k),1)+1j*np.random.randn(int(N/k),1))

        r=H*y.reshape(len(y),1)+w

        r=r/H #%Equalizer

        r = r.flatten()

        bitsOut = modulation.demodulate(r, 'hard')

        nPixels=64*48*3
        bitsPerPixel=24

        l = np.zeros(shape=(nPixels))
        
        for i in range(nPixels):
            inicio = (i-1) * bitsPerPixel + 1
            fim = inicio + bitsPerPixel - 1
            erros = sum(np.not_equal(bitsToTransmitte[inicio:fim], bitsOut[inicio:fim]))
            taxa = erros/bitsPerPixel
            if taxa <= limiteErro:
                l[i] = 1

        return l
    
def rgb_matrix_to_bits(rgb_matrix):
    height, width, _ = rgb_matrix.shape

    bits = []

    for row in range(height):
        for col in range(width):
            
            r, g, b = rgb_matrix[row, col]

            r_bin = format(r, '08b')  # 8 bits for red
            g_bin = format(g, '08b')  # 8 bits for green
            b_bin = format(b, '08b')  # 8 bits for blue

            rgb_bin = r_bin + g_bin + b_bin

            bits.extend([int(bit) for bit in rgb_bin])

    return bits