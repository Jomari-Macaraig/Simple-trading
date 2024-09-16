from django.db import transaction

from config.celery import app
from .constants import WalletTransactionType, WalletTransactionStatus
from .models import WalletTransaction


@app.task(name="wallet.process_wallet_transaction")
@transaction.atomic
def process_wallet_transaction(wallet_transaction_id: int):
    wallet_transaction = WalletTransaction.objects.get(pk=wallet_transaction_id)

    if wallet_transaction.status == WalletTransactionStatus.PENDING.value:
        amount = (
            wallet_transaction.amount
            if wallet_transaction.type == WalletTransactionType.DEPOSIT.value else
            -wallet_transaction.amount
        )
        wallet = wallet_transaction.wallet
        wallet.running_balance += amount

        if wallet.running_balance < 0:
            wallet_transaction.status = WalletTransactionStatus.INSUFFICIENT_FUNDS.value
            wallet_transaction.save()
        else:
            wallet_transaction.status = WalletTransactionStatus.COMPLETED.value
            wallet_transaction.save()
            wallet.save()