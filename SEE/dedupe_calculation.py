import datetime, binascii
import zlib
import hashlib
import time
import logging
import logging.handlers

LOGGER_NAME = 'dedupe_calculation.py'
LOG_FILENAME = 'logger_dedupe.log'
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*1024, backupCount=10)
FORMAT ="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
formatter = logging.Formatter(FORMAT,"%Y/%m/%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

filepath = "./logger_dedupe.log"
blocknum = 0
total_time_reading = 0
crc = 0
total_dupe_blocks = 0
dedupe_keys = {}
total_zero_blocks = 0
sampling_amount = 1

try:
    with open(filepath, "rb") as in_file:
        while True:
            blocknum += 1
            t1 = datetime.datetime.now()
            for i in range(0, sampling_amount):
                piece = in_file.read(4194304)
            t2 = datetime.datetime.now()
            total_time_reading += (t2 - t1).microseconds
            if piece == "":
                break

            """
            Check if zero-filled string, skip and continue.
            """
        print piece
        piece_sa = int(piece,2)
        #piece_sa = bin(int(binascii.hexlify(piece),16))
        print piece_sa
        print type(piece_sa)
        a = [1,2,3,0]
            #if all(byte for byte in piece): print "Zero blocks"
        #for i in piece_sa:
        #	print i
        if piece_sa == 0 : print "HAI"
        else: print "Hello"
            time.sleep(1)
            #m = hashlib.md5()

            for index in range(0, 512):
                crc = zlib.crc32(piece[0 + index * 8192:8192 + index * 8192], crc)
                if not crc & 0xffffffff in dedupe_keys:
                    dedupe_keys[crc & 0xffffffff] = 1
                else:
                    total_dupe_blocks += 1
            """
            
            start = 0
            size = 16384
            while start < len(piece):
                chunk = piece[start:start+size]
                #m.update(chunk)
                start += size
                crc = hashlib.md5(chunk).hexdigest()
                if not crc in dedupe_keys:
                    dedupe_keys[crc] = 1
                else:
                    total_dupe_blocks += 1
                    print ("otla dedupe blocks : %s" %str(total_dupe_blocks))
        """
except Exception, err:
    logger.error(str(err))
    raise Exception(err)

logger.debug("DEdupe keys : %s" % str(dedupe_keys))
logger.debug("Dedupe Length : %s" %(str(len(dedupe_keys))))
logger.debug("Total Dedupe blocks : %s" % str(total_dupe_blocks))
dedupe_ratio = total_dupe_blocks / (float(len(dedupe_keys)) + total_dupe_blocks)
logger.debug("Dedupe Ratio : %s" % str(format(dedupe_ratio, 'f')))
dedupe_ratio = format(dedupe_ratio, 'f')
logger.debug(dedupe_ratio)
