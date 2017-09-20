class ImageUtil {

    loadImage(src, opt_callback) {
        return new Promise((resolve) => {
            var canvas = document.createElement('canvas');
            var img = new window.Image();

            img.crossOrigin = '*';
            img.onload = function () {
                var context = canvas.getContext('2d');
                var imageData;

                canvas.width = img.width;
                canvas.height = img.height;
                context.drawImage(img, 0, 0, img.width, img.height);

                imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                resolve(imageData);
                img = null;
            };
            img.src = src;
        });
    };

    iterateImgData(imgData, cb) {
        for (let i = 0; i < imgData.height; i += imgData.width) {
            for (let j = i; j < imgData.width * (i + 1); j += 4) {
                cb(imgData.data[j], imgData.data[j + 1], imgData.data[j + 2], imgData.data[j + 3]);
            }
        }
    }

    grayscale(data) {
        for (var i = 0; i < data.length; i += 4) {
            var avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
            data[i] = avg; // red
            data[i + 1] = avg; // green
            data[i + 2] = avg; // blue
        }
    }

    toIndex(img, x, y){

        return x*4 + img.width*y;
    }
}

