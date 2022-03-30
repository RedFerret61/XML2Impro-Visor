#!/usr/bin/env python
# -*- coding: utf-8 -*-
# XML2Impro-Visor.py
#
# converts a musicxml file (or files in a directory) to impro-visor style leadsheet(s).
#
# Only converts chords not melody. Workaround:
# Example to rejoin melody to accompaniment (e.g. exported from Impro-visor):
#   In MuseScore, File > Open “accompaniment MIDI export”.mid
#   Edit > Instruments… add melody instrument
#   File > Open > original musicxml leadsheet with melody.mxl
#   Click on a note , select all (^A), copy ^C
#   Click on “accompaniment MIDI export” tab, scroll to new melody stave, select 2nd bar rest (if accompaniment has count in), Paste ^V
#
# free and open-source software, Paul Wardley Davies, see license.txt

# usage: XML2Impro-Visor.py [-h] [-m MXLFILEORPATHORPATH]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -m MXLFILEORPATH, --music MXLFILEORPATH
#                     music file or path, relative to current working directory e.g. XML2Impro-Visor/music.mxl or XML2Impro-Visor/leadsheets

# standard libraries
import argparse
import music21
from music21 import *
from music21 import stream, note, harmony
from music21.harmony import ChordSymbol, NoChord

import os
import sys

XML2IMPRO_VISOR_VERSION = '0.0.1'


def correct_chord(el):
    """
    given a music21.harmony.ChordSymbol return equivalent Impro-Visor 10.2 chord
    :param el: a music21.harmony.ChordSymbol
    :return: Impro-Visor chord
    """

    # remove spaces from chord
    chord = el.figure.replace(" ", "")

    if 'add#9' in chord:
        chord = chord.replace("add", "")

    if 'add4' in chord:
        chord = chord.replace("add", "sus")

    if 'o' in chord:
        chord = el.notes[0].name + el.chordKindStr

    if 'ø' in chord:
        chord = el.notes[0].name + el.chordKindStr

    chord = chord.replace("-", "b")
    return chord


class ImprovisorLeadsheet:
    """
    A class that stores an ImprovisorLeadsheet
    """
    # class variables shared by all instances
    # None

    # class instantiation automatically invokes __init__
    def __init__(self, name, song_stream):
        """
        takes song_key
        and initialises section data
        """
        # update class variables
        self.name = name
        self.song_stream = song_stream
        self.meter = '4 4'

        first_time_sig = self.get_first_time_sig(song_stream)
        # print('first time sig', first_time_sig)
        # print(first_time_sig.numerator, '/', first_time_sig.denominator)
        self.meter = str(first_time_sig.numerator) + ' ' + str(first_time_sig.denominator)
        # print('self.meter', self.meter)

        self.key = 0
        first_key_signature = self.get_first_key_signature()
        # print('first_key_signature.number',first_key_signature.number)
        self.key = first_key_signature.sharps

        self.composer = 'XML2Impro-Visor.py ' + XML2IMPRO_VISOR_VERSION
        self.tempo = 120.0

        first_tempo = self.get_first_tempo()
        # print('first_tempo.number',first_tempo.number)
        self.tempo = first_tempo.number

        self.volume = 127
        self.bass_volume = 100
        self.drum_volume = 100
        self.chord_volume = 100

        print('')
        print('creating Impro-Visor leadsheet...')
        self.lines = []
        self.nl = '\n'

        # metadata
        print('creating metadata...')

        title_line = '(title ' + self.name + ')'
        self.lines += [title_line, self.nl]

        meter_line = '(meter ' + self.meter + ')'
        self.lines += [meter_line, self.nl]

        key_line = '(key ' + str(self.key) + ')'
        self.lines += [key_line, self.nl]

        composer_line = '(composer ' + self.composer + ')'
        self.lines += [composer_line, self.nl]

        tempo_line = '(tempo ' + str(self.tempo) + ')'
        self.lines += [tempo_line, self.nl]

        volume_line = '(volume ' + str(self.volume) + ')'
        self.lines += [volume_line, self.nl]

        bass_volume_line = '(bass-volume ' + str(self.bass_volume) + ')'
        self.lines += [bass_volume_line, self.nl]

        drum_volume_line = '(drum-volume ' + str(self.drum_volume) + ')'
        self.lines += [drum_volume_line, self.nl]

        chord_volume_line = '(chord-volume ' + str(self.chord_volume) + ')'
        self.lines += [chord_volume_line, self.nl]

        # style (overrides Impro-visor default)
        if self.meter == '3 4':
            self.lines += ['(section (style waltz))', self.nl]

        if self.meter == '4 4':
            self.lines += ['(section (style rock-medium))', self.nl]

        # chords
        self.init_chords()

        # print('lines', self.lines)
        return

    def get_first_key_signature(self):
        """
        :return: first key signature or if None return a key.KeySignature with zero sharps (C)
        """
        ks = key.KeySignature(0)
        try:
            ks = self.song_stream[music21.key.KeySignature][0]
        except IndexError as error:
            ks = key.KeySignature(0)

        return ks

    def get_first_tempo(self):
        """
        :param a_stream: of music
        :return: the first tempo
        """

        first = True
        for sT in self.song_stream.flat.getElementsByClass('MetronomeMark'):
            if first:
                songTempo = sT
                # print('First Tempo:', songTempo)
                first = False
            else:
                print('other Tempo:', sT)
        if first == True:
            songTempo = tempo.MetronomeMark(number=120)
        return songTempo

    def get_first_time_sig(self, a_stream):
        """
        :param a_stream: of music
        :return: the first time signature
        """
        # may have to get first part
        # myPart[music21.meter.TimeSignature][0]

        return a_stream[music21.meter.TimeSignature][0]

    def init_chords(self):
        """
        parse the stream to add chords to the lines
        for each measure
            for each note
                if note has chord:
                    add chord to line
                    add space to line
            add end measure bar to line
            add space to line
        add line to lines
        :return: void
        """
        print('creating chords...')
        chord_line = ''

        for p in self.song_stream.parts:

            # foreach measure
            for i, m in enumerate(p.getElementsByClass('Measure')):
                # print('part', p,'measure', m,'measureIndex', i )
                # foreach element
                no_chord = True
                for count_el, el in enumerate(m.flat):
                    # if type(el) == music21.note.Rest or type(el) == music21.note.Note:
                    #     print('note/rest',el)
                    if type(el) == music21.harmony.ChordSymbol:
                        # print('chord figure ', el.figure, 'notes[0].name', el.notes[0].name, 'chordKindStr', el.chordKindStr )
                        corrected_chord = correct_chord(el)
                        # chord_line += str(el.figure) + ' '
                        chord_line += str(corrected_chord) + ' '
                        no_chord = False
                if no_chord == True:
                    chord_line += 'NC '
                chord_line +=  '| '
        # print('chord_line',chord_line)
        self.lines += [chord_line, self.nl]

    def write(self, ls_file_fully_qualified):
        print('writing Impro-Visor Leadsheet...', ls_file_fully_qualified)
        with open(ls_file_fully_qualified, 'w') as f:
            f.writelines(self.lines)



def main():
    """
    parse command line arguments
    read mxl
    convert stream to ls leadsheet
    write ls leadsheet
    """

    # Specify command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--MXLFILEORPATH',
                        help='music file or path, relative to current working directory e.g. XML2Impro-Visor/music.mxl or XML2Impro-Visor/leadsheets',
                        default='',
                        type=str)

    # print the help message only if no arguments are supplied on the command line
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse command line arguments.
    args = parser.parse_args()
    print('')
    print("MXLFILEORPATH fully qualified:", args.MXLFILEORPATH)

    if os.path.isdir(args.MXLFILEORPATH):
        print("MXLFILEORPATH is a directory")
        mxl_files = [f for f in os.listdir(args.MXLFILEORPATH) if f.endswith('.mxl')]
        mxlfile_path = os.curdir + os.sep + args.MXLFILEORPATH

    else:
        print("MXLFILEORPATH is a file")
        mxl_files = [os.path.basename(args.MXLFILEORPATH)]
        MXLFILEORPATH_path = os.path.dirname(args.MXLFILEORPATH)
        mxlfile_path = os.curdir + os.sep + MXLFILEORPATH_path

    if mxl_files == []:
        print('exit: Error no mxl_files found', args.MXLFILEORPATH)
        sys.exit()

    # print('MXLFILEORPATH, mxl_files', args.MXLFILEORPATH,  mxl_files)
    # print('mxlfile_path', mxlfile_path)

    # read mxl
    for mxl_file in mxl_files:
        mxl_file_fully_qualified = mxlfile_path + os.sep + mxl_file
        # print('mxl_file ',mxl_file )
        print('mxl_file_fully_qualified:', mxl_file_fully_qualified )
        if not os.path.isfile(mxl_file_fully_qualified):
            print('exit: Error mxl_file not found', mxl_file_fully_qualified)
            sys.exit()

        mxl_leadsheet = music21.converter.parse(mxl_file_fully_qualified)
        # mxl_leadsheet.show('text')
        # input('Press Enter to continue...')

        ls_file = os.path.splitext(mxl_file)[0] + '.ls'
        ls_file_fully_qualified = mxlfile_path + os.sep + ls_file

        # initialise Improvisor Leadsheet with mxl_leadsheet (which convert stream to ls leadsheet)
        imp_ls = ImprovisorLeadsheet(os.path.splitext(ls_file)[0], mxl_leadsheet)

        # write improvisor ls leadsheet
        imp_ls.write(ls_file_fully_qualified)
        # a_song.write(fp=MXLFILEORPATH_normalised_name_path) # write normalised score to musicxml file

        print('output file contents:')
        print('')

        with open(ls_file_fully_qualified, 'r') as fin:
            print(fin.read())

if __name__ == '__main__':

    main()
