import { parseFile } from 'music-metadata';
// import { inspect } from 'util';

(async () => {
    try {
        const metadata = await parseFile('/media/auishik/Official/audio_specs_js/audio_files/8577.wav');
        console.log(metadata.format);
    } catch (error) {
        console.error('{container: "Unknown"}');
}
})();