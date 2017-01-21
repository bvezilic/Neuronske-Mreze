import cv2


car_height = 58.5
camera_height = 150
image_height = 144

def detect_cars(image):
    # constants
    IMAGE_SIZE = 200.0
    MATCH_THRESHOLD = 15
    #print image.shape
    #cascade_url = 'frontal_stop_sign_cascade.xml'
    cascade_url = 'cars.xml'
    img_url = 'Cars/car2.jpg'
    roundabout_cascade = cv2.CascadeClassifier(cascade_url)
    street = image #cv2.imread(img_url)
    #street = cv2.resize(street, (300, 300))

    # detekcija znaka na slici
    gray = cv2.cvtColor(street, cv2.COLOR_RGB2GRAY)
    signs = roundabout_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1
    )
    #print signs
    #orb i feature matcher
    orb = cv2.ORB()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # kljucne karakteristike za znake koje sluze za odbacivanje lose prepoznatih delova
    roadsign = cv2.imread('orb_feature.jpg', 0)
    kp_r, des_r = orb.detectAndCompute(roadsign, None)

    # prolazak kroz sve znake
    for (x, y, w, h) in signs:

        # vadjenje objekta
        obj = gray[y:y + h, x:x + w]
        ratio = IMAGE_SIZE / obj.shape[1]
        obj = cv2.resize(obj, (int(IMAGE_SIZE), int(obj.shape[0] * ratio)))

        # pronalazenje karakteristika na slici
        kp_o, des_o = orb.detectAndCompute(obj, None)
        if len(kp_o) == 0 or des_o == None: continue

        matches = bf.match(des_r, des_o)

        # obelezavanje detektovanog znaka
        #if (len(matches) >= MATCH_THRESHOLD):
        cv2.rectangle(street, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #print 'Koordinate: {0}, '.format((x, y, w, h))
        distance = (car_height*image_height)/y*camera_height
        print distance

        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)



    return street
    # cv2.imshow('stop', street)
    # cv2.waitKey(3000000)
    # cv2.destroyAllWindows()