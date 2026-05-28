import cv2
import numpy as np

def detect_sift(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = gray_image.shape[:2]
    kp_distance_limit = max(height,width)*0.06

    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches =bf.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    for m, n, p in matches:
        score  = n.distance / p.distance

        pt1 = keypoints[n.queryIdx].pt
        pt2 = keypoints[n.trainIdx].pt

        kp_distance = np.linalg.norm(np.array(pt1)-np.array(pt2))

        if score < 0.60 and kp_distance > kp_distance_limit:
            good_matches.append(n)
    draw_matches = cv2.drawMatches(image, keypoints, image, keypoints, good_matches, None)

    return {
        "keypoint_count": len(keypoints),
        "match_count": len(good_matches),
        "is_forged":True if len(good_matches) > 10 else False,
        "result_image": draw_matches
}

def detect_orb(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = gray_image.shape[:2]
    kp_distance_limit = max(height,width)*0.060

    orb = cv2.ORB_create(nfeatures=2500)
    keypoints, descriptors = orb.detectAndCompute(gray_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    for m, n, p in matches:
        score = n.distance / p.distance

        pt1 = keypoints[n.queryIdx].pt
        pt2 = keypoints[n.trainIdx].pt

        kp_distance = np.linalg.norm(np.array(pt1)-np.array(pt2))

        if score < 0.63 and kp_distance > kp_distance_limit:
            good_matches.append(n)
    
    draw_matches = cv2.drawMatches(image, keypoints, image, keypoints, good_matches, None)

    return {
        "keypoint_count": len(keypoints),
        "match_count": len(good_matches),
        "is_forged":True if len(good_matches) > 10 else False,
        "result_image": draw_matches
}

def detect_akaze(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = gray_image.shape[:2]
    kp_distance_limit = max(height,width)*0.04

    akaze = cv2.AKAZE_create()
    keypoints, descriptors = akaze.detectAndCompute(gray_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    for m, n, p in matches:
        score = n.distance / p.distance

        pt1 = keypoints[n.queryIdx].pt
        pt2 = keypoints[n.trainIdx].pt

        kp_distance = np.linalg.norm(np.array(pt1)-np.array(pt2))

        if score < 0.70 and kp_distance > kp_distance_limit:
            good_matches.append(n)
    
    draw_matches = cv2.drawMatches(image, keypoints, image, keypoints, good_matches, None)

    return {
        "keypoint_count": len(keypoints),
        "match_count": len(good_matches),
        "is_forged":True if len(good_matches) > 10 else False,
        "result_image": draw_matches
}

def detect_brisk(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = gray_image.shape[:2]
    kp_distance_limit = max(height,width)*0.04

    brisk = cv2.BRISK_create()
    keypoints, descriptors = brisk.detectAndCompute(gray_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    for m, n, p in matches:
        score = n.distance / p.distance

        pt1 = keypoints[n.queryIdx].pt
        pt2 = keypoints[n.trainIdx].pt

        kp_distance = np.linalg.norm(np.array(pt1)-np.array(pt2))

        if score < 0.70 and kp_distance > kp_distance_limit:
            good_matches.append(n)
    
    draw_matches = cv2.drawMatches(image, keypoints, image, keypoints, good_matches, None)

    return {
        "keypoint_count": len(keypoints),
        "match_count": len(good_matches),
        "is_forged":True if len(good_matches) > 10 else False,
        "result_image": draw_matches
}
