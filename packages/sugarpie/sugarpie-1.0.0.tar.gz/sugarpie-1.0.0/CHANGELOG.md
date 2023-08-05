1.0.0:
- Add the boot watchdog feature (it has an [open issue](https://github.com/PiSugar/pisugar-power-manager-rs/issues/81))
- breaking change in the API that triggers a major version number bump:
	- the call to turn_on / off_system_watchdog() is now replaced
	  with switch_system_watchdog('on' / 'off')
