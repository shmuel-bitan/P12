class Serializer:
    def __init__(self, data):
        self.data = data
        self.validated_data = {}
        self.errors = {}

    def is_valid(self):
        raise NotImplementedError


class ClientSerializer(Serializer):
    def is_valid(self):
        required_fields = ['full_name', 'email', 'phone', 'company_name', 'sales_contact_id']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = 'This field is required'
        if not self.errors:
            self.validated_data = self.data
            return True
        return False


class ContractSerializer(Serializer):
    def is_valid(self):
        required_fields = ['client_id', 'sales_contact_id', 'total_amount', 'amount_due', 'status']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = 'This field is required'
        if not self.errors:
            self.validated_data = self.data
            return True
        return False


class EventSerializer(Serializer):
    def is_valid(self):
        required_fields = ['contract_id', 'event_name', 'client_id', 'client_contact', 'event_date_start',
                           'event_date_end', 'support_contact_id', 'location', 'attendees']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = 'This field is required'
        if not self.errors:
            self.validated_data = self.data
            return True
        return False
