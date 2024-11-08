from enum import Enum


class DocumentTypes(Enum):
    INVOICE = "invoices"
    INVOICE_RECEIPT = "invoice_receipts"
    PASSPORT = "passports"
    DRIVING_LICENSE = "driving_licenses"
    BANK_STATEMENT = "bank_statements"
    INVOICE_OLD = "invoices_old"
