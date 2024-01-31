FROM amd64/ubuntu:18.04 AS base

EXPOSE 8788/tcp
EXPOSE 9766/tcp

ENV DEBIAN_FRONTEND=noninteractive

#Add ppa:bitcoin/bitcoin repository so we can install libdb4.8 libdb4.8++
RUN apt-get update && \
	apt-get install -y software-properties-common && \
	add-apt-repository ppa:bitcoin/bitcoin

#Install runtime dependencies
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	bash net-tools libminiupnpc10 \
	libevent-2.1 libevent-pthreads-2.1 \
	libdb4.8 libdb4.8++ \
	libboost-system1.65 libboost-filesystem1.65 libboost-chrono1.65 \
	libboost-program-options1.65 libboost-thread1.65 \
	libzmq5 && \
	apt-get clean

FROM base AS build

#Install build dependencies
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	bash net-tools build-essential libtool autotools-dev automake git \
	pkg-config libssl-dev libevent-dev bsdmainutils python3 \
	libboost-system1.65-dev libboost-filesystem1.65-dev libboost-chrono1.65-dev \
	libboost-program-options1.65-dev libboost-test1.65-dev libboost-thread1.65-dev \
	libzmq3-dev libminiupnpc-dev libdb4.8-dev libdb4.8++-dev && \
	apt-get clean


#Build Bitcoin69 from source
COPY . /home/btc69/build/Bitcoin69/
WORKDIR /home/btc69/build/Bitcoin69
RUN ./autogen.sh && ./configure --disable-tests --with-gui=no && make

FROM base AS final

#Add our service account user
RUN useradd -ms /bin/bash btc69 && \
	mkdir /var/lib/btc69 && \
	chown btc69:btc69 /var/lib/btc69 && \
	ln -s /var/lib/btc69 /home/btc69/.btc69 && \
	chown -h btc69:btc69 /home/btc69/.btc69

VOLUME /var/lib/btc69

#Copy the compiled binaries from the build
COPY --from=build /home/btc69/build/Bitcoin69/src/btc69d /usr/local/bin/btc69d
COPY --from=build /home/btc69/build/Bitcoin69/src/btc69-cli /usr/local/bin/btc69-cli

WORKDIR /home/btc69
USER btc69

CMD /usr/local/bin/btc69d -datadir=/var/lib/btc69 -printtoconsole -onlynet=ipv4
