## Guitar Tab Generator

### Description:
This application produces professional guitar tablature using [VexFlow's](https://vexflow.com/) notation API from a music file assumed to be containing guitar music.

### Roadmap:
  - **Data Analysis**:
    - [x] Find a way to parse music files in python
    - [x] Figure out how to correctly apply a Fast Fourier Transform (FFT) to an auido file
    - [ ] Write a peak finding algorithm that extracts the peaks of the FFT (IN PROGRESS)
    - [ ] Filter overtones while keeping every fundamental pitches (might have something to do with the relative size of the peaks that follow a given peak in the harmoinc series)
    - [x] Map peaks in the FFT to possible positions on the fretboard
    - [ ] Once an algorithm that consistently identifies notes in a snapshot in time, divide the the whole audio file into discrete bins and apply the FFT to all
    - [ ] Optimize bin size and figure out how to identify repitions among neighbouring bins
    - [ ] Map this output to VexFlow's tab syntax
  - **Visual**:
    - [ ] Setup a flask server using Tailwind CSS
    - [ ] Spend time creating a presentable layout and theme
    - [ ] Create a drag and drop system for music files (HARD?)
    - [ ] Place the tab generated from VexFlow's tab API on the page


### Comments:
The project was created so that evidence of its inception is documented, but this does not have any functionality as is currently a play area as a means of figuring out how to implement the data analysis portion.
