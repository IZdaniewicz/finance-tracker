const fs = require('fs');
const path = require('path');

const sourceDir = './src';
const destinationDir = './public';

fs.readdir(sourceDir, (err, files) => {
  if (err) throw err;

  files.filter(file => path.extname(file) === '.html')
    .forEach(file => {
      const sourcePath = path.join(sourceDir, file);
      const destinationPath = path.join(destinationDir, file);
      
      fs.copyFile(sourcePath, destinationPath, err => {
        if (err) throw err;
        console.log(`${file} copied to ${destinationDir}`);
      });
    });
});

fs.watch('./src/', (eventType, filename) => {
    if (filename.endsWith('.html') && eventType === 'change') {
        fs.copyFile(`./src/${filename}`, `./public/${filename}`,
            (err) => {
                err ? console.log(err) : console.log(`${filename} copied!\n`);
            });
    }
});
