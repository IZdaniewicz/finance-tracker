const fs = require('fs');
var i = 0;
fs.watch('./src/', (eventType, filename) => {
    // console.log(`${i}->${filename}:${eventType} out!\n`);
    // i++;
    if (filename.endsWith('.html') && eventType === 'change') {
        fs.copyFile(`./src/${filename}`, `./public/${filename}`,
            (err) => {
                err ? console.log(err) : console.log(`${filename} copied!\n`);
            });
    }
});
