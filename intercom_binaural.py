# Exploiting binaural redundancy.

from intercom_bitplanes import Intercom_bitplanes
import struct
import numpy as np

class Intercom_binaural(Intercom_bitplanes):

    def init(self, args):
        Intercom_bitplanes.init(self, args)
        if self.number_of_channels == 2:
            self.record_send_and_play = self.record_send_and_play_stereo

    def record_send_and_play_stereo(self, indata, outdata, frames, time, status):
        indata[:, 0] -= indata[:,1] #RESTAMOS AMBOS CANALES
        self.send(indata) #MANDAMOS LA DIFERENCIA PERO PASANDO AMBOS CANALES
        self.recorded_chunk_number = (self.recorded_chunk_number + 1) % self.MAX_CHUNK_NUMBER #ELEVAMOS EL CONTADOR DEL BUFFER PARA TRABAJAR PARA CON EL CHUNK
        chunk_buffer = self._buffer[self.played_chunk_number % self.cells_in_buffer] #COGENOS EL CHUNK DEL BUFFER 
        chunk_buffer[:,0] += chunk_buffer[:,1] #DESHACEMOS LA DIFERENCIA
        self._buffer[self.played_chunk_number % self.cells_in_buffer] = self.generate_zero_chunk()
        self.played_chunk_number = (self.played_chunk_number + 1) % self.cells_in_buffer #AUMENTAMOS EL CONTADOR DE REPRODUCCIÓN DEL BUFFER
        outdata[:] = chunk_buffer #MANDAMOS A LA TARJETA DE SONIDO EL CHUNK
        

        
if __name__ == "__main__":
    intercom = Intercom_binaural()
    parser = intercom.add_args()
    args = parser.parse_args()
    intercom.init(args)
    intercom.run()
