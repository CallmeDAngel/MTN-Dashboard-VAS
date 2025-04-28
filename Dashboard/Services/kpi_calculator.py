class KPICalculator:
        @staticmethod
        def calculate(kpi_name, platform_name, data):
                method_name = f"_calculate_{kpi_name.lower()}_{platform_name.lower()}"
                method = getattr(KPICalculator, method_name, None)
                if method:
                        return method(data)
                raise NotImplementedError(f"No calculation method for {kpi_name} on {platform_name}")

        
        #DMC
        @staticmethod
        def _calculate_qos_dmc(data):
                # Implémentez le calcul spécifique ici
                pass

        @staticmethod
        def _calculate_usage_rate_dmc(data):
                # Implémentez le calcul spécifique ici
                pass
        
        
        #EIR
        @staticmethod
        def _calculate_calcul_qos_EIR(data):
                # Logique spécifique
                pass
        
        @staticmethod
        def _calcul_usage_rate_EIR(data):
                # Logique spécifique
                pass
        
        #VMS
        @staticmethod
        def _calcul_qos_VMS(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_VMS(data):
                # Logique spécifique
                pass

        #MCN
        @staticmethod
        def _calcul_qos_MCN(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_MCN(data):
                # Logique spécifique
                pass
                
        #IVR
        @staticmethod
        def _calcul_qos_IVR(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_IVR(data):
                # Logique spécifique
                pass
                
        #OBD
        @staticmethod
        def _calcul_qos_OBD(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_OBD(data):
                # Logique spécifique
                pass
                
        #COLLECT_CALL
        @staticmethod
        def _calcul_qos_COLLECT_CALL(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_COLLECT_CALL(data):
                # Logique spécifique
                pass
                
        #AUTOCALL_COMPLETION
        @staticmethod
        def _calcul_qos_AUTOCALL_COMPLETION(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_AUTOCALL_COMPLETION(data):
                # Logique spécifique
                pass
                
        #CRBT
        @staticmethod
        def _calcul_qos_CRBT(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_CRBT(data):
                # Logique spécifique
                pass
                
        #SMS_PRO
        @staticmethod
        def _calcul_qos_SMS_PRO(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_SMS_PRO(data):
                # Logique spécifique
                pass
                
        #SMS
        @staticmethod
        def _calcul_qos_SMS(data):
                #P2P calcul
                pass

        @staticmethod
        def _calcul_usage_rate_SMS(data):
                # Logique spécifique
                pass
                
        #USSD
        @staticmethod
        def _calcul_qos_USSD(data):
                # Logique spécifique
                pass

        @staticmethod
        def _calcul_usage_rate_USSD(data):
                # Logique spécifique
                pass

        # Ajoutez d'autres méthodes de calcul pour chaque combinaison de KPI et plateforme