class ImageManipulator{
    histogram(image){
        let hist = new Array(256).fill(0);
        for(let i = 0; i < image.data.length; i++){
            hist[image.data[i]]++;
        }
        return hist;
    }

    max(img){
        return img.data.reduce((rest, next) => {
            return rest > next ? rest : next;
        });
    }

}

// hist = np.zeros(256, dtype='uint8')
// for i in range(h):
//     for j in range(w):
//         hist[image[i][j]] += 1
// return hist
