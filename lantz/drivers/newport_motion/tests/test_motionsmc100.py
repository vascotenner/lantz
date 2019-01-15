if __name__ == '__main__':
    import argparse
    import lantz.log

    parser = argparse.ArgumentParser(description='Test SMC100 driver')
    parser.add_argument('-p', '--port', type=str, default='1',
                        help='Serial port to connect to')

    args = parser.parse_args()
    lantzlog = lantz.log.log_to_screen(level=lantz.log.INFO)
    lantz.log.log_to_socket(lantz.log.DEBUG)

    import lantz
    import visa
    import lantz.drivers.newport_motion
    from lantz.drivers.newport_motion import SMC100
    rm = visa.ResourceManager('@py')
    lantz.messagebased._resource_manager = rm

    print(lantz.messagebased._resource_manager.list_resources())

    with SMC100(args.port) as inst:
    #with sm.via_serial(port=args.port) as inst:
        inst.idn
        # inst.initialize() # Initialize the communication with the power meter
        # Find the status of all axes:
        #for axis in inst.axes:
        #    print('Axis {} Position {} is_on {} max_velocity {} velocity {}'.format(axis.num, axis.position,
        #                                                                            axis.is_on, axis.max_velocity,
        #                                                                            axis.velocity))
