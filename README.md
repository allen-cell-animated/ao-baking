## Exporting from UCSF Chimera
1. You need to use original chimera because it saves nested obj files. [UCSF Chimera](https://www.cgl.ucsf.edu/chimera/download.html)
2. Your script should 
  * open all the files, 
  * set voxelSize (if needs to be adjusted) `volume # voxelSize 0.065,0.065,0.29;` 
  * set the step `volume # step 1;`
  * set the level, `volume #0 level 0.0562;`
  * and then save it as an .obj: `export ${exportPath}/mitochondria-M1.obj;`
Example template: 
```JavaScript
const exportPath = '/Users/meganr/Dropbox/visual_cell_maker_files/objs-to-process'
module.exports = (mitosis, structure, voxelSize, memLevel, dnaLevel, structureLevel) =>
  `open /Users/meganr/Dropbox/visual_cell_maker_files/${structure}/${mitosis}/*.tiff;

volume # voxelSize ${voxelSize};

volume # step 1;
volume #0 level ${memLevel};
volume #1 level ${dnaLevel};
volume #2 level ${structureLevel};

export ${exportPath}/${structure}-${mitosis}.obj;

close all;
```

# ao-baking

1. Open C4D
2. In UV-editing mode select 'UV Mesh' and then 'Show UV Mesh' (we tried to script this, but it doesnt seem to work)
3. Go back to standard/startup view if you want to watch the console. 
4. Run script 'visual-cell.py'

## Editing the script 
Things you'll need to change:
* Input path (where the Objs are located, you can use the dropbox folder if you have that locally)
* Output path (where you are going to save these, it needs the actual file structure to exist, so you can copy my dropbox folder. It will overwrite exisiting images. 
* fileNames (the structures + mitotic stages you want to process)
